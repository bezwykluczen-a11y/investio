#!/usr/bin/env python3
"""
Przygotowuje pliki produkcyjne dla deploymentu na Hetzner
(domena: spolki-niemieckie.pl / punycode: xn--spki-niemieckie-xrb.pl).

Tworzy:
  - docker-compose.prod.yml      (produkcyjny stack + nginx)
  - infra/nginx/nginx.conf       (reverse proxy dla 3 subdomen)
  - frontend/Dockerfile.prod     (produkcyjny build Next.js)
  - backend/.env.production.example
  - DEPLOYMENT.md                (instrukcja krok po kroku)

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 prepare_production.py

Potem postepuj wg DEPLOYMENT.md.
"""
import os

DOMAIN_PUNYCODE = "xn--spki-niemieckie-xrb.pl"

FILES: dict[str, str] = {}

FILES["docker-compose.prod.yml"] = f'''services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: portal
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD}}
      POSTGRES_DB: portal
    volumes:
      - db_data:/var/lib/postgresql/data
    expose:
      - "5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U portal"]
      interval: 10s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    expose:
      - "6379"

  minio:
    image: minio/minio:latest
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${{MINIO_ROOT_USER}}
      MINIO_ROOT_PASSWORD: ${{MINIO_ROOT_PASSWORD}}
    volumes:
      - minio_data:/data
    expose:
      - "9000"

  api:
    build:
      context: .
      dockerfile: infra/docker/Dockerfile.backend
    restart: unless-stopped
    env_file:
      - backend/.env.production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    expose:
      - "8000"

  worker:
    build:
      context: .
      dockerfile: infra/docker/Dockerfile.backend
    restart: unless-stopped
    command: celery -A app.worker worker --loglevel=info
    env_file:
      - backend/.env.production
    depends_on:
      - redis
      - db

  web:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        NEXT_PUBLIC_API_URL: https://api.{DOMAIN_PUNYCODE}/api/v1
        WORDPRESS_API_URL: https://blog.{DOMAIN_PUNYCODE}/wp-json/wp/v2
    restart: unless-stopped
    depends_on:
      - api
      - wordpress
    expose:
      - "3000"

  wordpress-db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: ${{WORDPRESS_DB_PASSWORD}}
      MYSQL_ROOT_PASSWORD: ${{WORDPRESS_DB_ROOT_PASSWORD}}
    volumes:
      - wordpress_db_data:/var/lib/mysql
    expose:
      - "3306"

  wordpress:
    image: wordpress:latest
    restart: unless-stopped
    environment:
      WORDPRESS_DB_HOST: wordpress-db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: ${{WORDPRESS_DB_PASSWORD}}
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_CONFIG_EXTRA: |
        define('WP_HOME', 'https://blog.{DOMAIN_PUNYCODE}');
        define('WP_SITEURL', 'https://blog.{DOMAIN_PUNYCODE}');
        if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {{
            $_SERVER['HTTPS'] = 'on';
        }}
    depends_on:
      - wordpress-db
    volumes:
      - wordpress_data:/var/www/html
    expose:
      - "80"

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infra/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./infra/nginx/certbot/conf:/etc/letsencrypt
      - ./infra/nginx/certbot/www:/var/www/certbot
    depends_on:
      - web
      - api
      - wordpress

  certbot:
    image: certbot/certbot
    restart: unless-stopped
    volumes:
      - ./infra/nginx/certbot/conf:/etc/letsencrypt
      - ./infra/nginx/certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  db_data:
  minio_data:
  wordpress_data:
  wordpress_db_data:
'''

FILES["infra/nginx/nginx.conf"] = f'''user nginx;
worker_processes auto;
events {{ worker_connections 1024; }}

http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    client_max_body_size 20m;

    map $http_upgrade $connection_upgrade {{
        default upgrade;
        '' close;
    }}

    # --- HTTP -> HTTPS redirect + ACME challenge ---
    server {{
        listen 80;
        server_name {DOMAIN_PUNYCODE} www.{DOMAIN_PUNYCODE} api.{DOMAIN_PUNYCODE} blog.{DOMAIN_PUNYCODE};

        location /.well-known/acme-challenge/ {{
            root /var/www/certbot;
        }}

        location / {{
            return 301 https://$host$request_uri;
        }}
    }}

    # --- Frontend (Next.js) ---
    server {{
        listen 443 ssl;
        server_name {DOMAIN_PUNYCODE} www.{DOMAIN_PUNYCODE};

        ssl_certificate     /etc/letsencrypt/live/{DOMAIN_PUNYCODE}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{DOMAIN_PUNYCODE}/privkey.pem;

        location / {{
            proxy_pass http://web:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }}
    }}

    # --- Backend (FastAPI) ---
    server {{
        listen 443 ssl;
        server_name api.{DOMAIN_PUNYCODE};

        ssl_certificate     /etc/letsencrypt/live/api.{DOMAIN_PUNYCODE}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.{DOMAIN_PUNYCODE}/privkey.pem;

        location / {{
            proxy_pass http://api:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}

    # --- WordPress (blog headless) ---
    server {{
        listen 443 ssl;
        server_name blog.{DOMAIN_PUNYCODE};

        ssl_certificate     /etc/letsencrypt/live/blog.{DOMAIN_PUNYCODE}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/blog.{DOMAIN_PUNYCODE}/privkey.pem;

        location / {{
            proxy_pass http://wordpress:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
}}
'''

FILES["frontend/Dockerfile.prod"] = '''FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json ./
RUN npm install

FROM node:20-alpine AS builder
WORKDIR /app
ARG NEXT_PUBLIC_API_URL
ARG WORDPRESS_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV WORDPRESS_API_URL=$WORDPRESS_API_URL
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "run", "start"]
'''

FILES["backend/.env.production.example"] = f'''ENVIRONMENT=production
SECRET_KEY=UZUPELNIC-losowy-64-znakowy-ciag
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+psycopg2://portal:UZUPELNIC-haslo-db@db:5432/portal
REDIS_URL=redis://redis:6379/0
CORS_ORIGINS=https://{DOMAIN_PUNYCODE},https://www.{DOMAIN_PUNYCODE}
STORAGE_BUCKET=portal-documents
STORAGE_ENDPOINT_URL=http://minio:9000
STORAGE_ACCESS_KEY=UZUPELNIC
STORAGE_SECRET_KEY=UZUPELNIC
MAX_UPLOAD_MB=15
'''

FILES["DEPLOYMENT.md"] = f'''# Deployment na Hetzner - spolki-niemieckie.pl

Domena (punycode): `{DOMAIN_PUNYCODE}`
Serwer: `77.42.64.51`

## Krok 0: DNS

W panelu zarzadzania domena dodaj rekordy A wskazujace na `77.42.64.51`:

| Rekord | Wartosc |
|---|---|
| `@` | 77.42.64.51 |
| `www` | 77.42.64.51 |
| `api` | 77.42.64.51 |
| `blog` | 77.42.64.51 |

Poczekaj na propagacje (zwykle 5-30 min). Sprawdz: `nslookup api.{DOMAIN_PUNYCODE}`.

## Krok 1: Przygotowanie serwera (SSH)

```bash
ssh root@77.42.64.51

# aktualizacja systemu
apt update && apt upgrade -y

# Docker + compose plugin
curl -fsSL https://get.docker.com | sh
apt install -y docker-compose-plugin

# katalog projektu
mkdir -p /opt/investio
```

UWAGA: jesli na serwerze dziala juz inny nginx/apach albo inne kontenery
z portami 80/443 - najpierw je zatrzymaj (`docker ps`, `systemctl status nginx`).

## Krok 2: Wgranie kodu na serwer

Na lokalnym komputerze (PowerShell), w folderze projektu:

```powershell
cd C:\\Users\\bezwy\\portal-zbiorek-mvp\\mvp-portal-projektow
git init
git add .
git commit -m "MVP + produkcja"
```

Najprosciej: zaloz prywatne repo na GitHub i na serwerze `git clone`.
Alternatywnie (bez gita), spakuj i wyslij przez scp:

```powershell
# PowerShell (lokalnie)
tar -czf investio.tar.gz --exclude=node_modules --exclude=.next --exclude=__pycache__ .
scp investio.tar.gz root@77.42.64.51:/opt/investio/
```

Na serwerze:

```bash
cd /opt/investio
tar -xzf investio.tar.gz
```

## Krok 3: Konfiguracja produkcyjna

```bash
cd /opt/investio
cp backend/.env.production.example backend/.env.production
nano backend/.env.production   # uzupelnij SECRET_KEY i hasla
```

Wygeneruj SECRET_KEY: `openssl rand -hex 32`.

Utworz plik z haslami dla compose:

```bash
nano /opt/investio/.env
```

Zawartosc:

```
POSTGRES_PASSWORD=...losowe...
MINIO_ROOT_USER=investio
MINIO_ROOT_PASSWORD=...losowe...
WORDPRESS_DB_PASSWORD=...losowe...
WORDPRESS_DB_ROOT_PASSWORD=...losowe...
```

## Krok 4: Certyfikaty SSL (pierwsze uruchomienie)

Najpierw tymczasowo uruchom nginx bez certow (katalog challenge):

```bash
cd /opt/investio
mkdir -p infra/nginx/certbot/conf infra/nginx/certbot/www
docker compose -f docker-compose.prod.yml up -d db redis minio wordpress-db wordpress
docker compose -f docker-compose.prod.yml up -d nginx certbot
```

Jesli nginx nie wstanie przez brak certow, tymczasowo zakomentuj bloki
`server {{ listen 443 ... }}` w nginx.conf, zostaw tylko listen 80.

Wystaw certyfikaty:

```bash
docker compose -f docker-compose.prod.yml run --rm certbot certonly \\
  --webroot -w /var/www/certbot \\
  -d {DOMAIN_PUNYCODE} -d www.{DOMAIN_PUNYCODE} \\
  -d api.{DOMAIN_PUNYCODE} -d blog.{DOMAIN_PUNYCODE} \\
  --email twoj@email.pl --agree-tos --no-eff-email
```

Po sukcesie przywroc pelny nginx.conf (z blokami 443) i:

```bash
docker compose -f docker-compose.prod.yml restart nginx
```

## Krok 5: Build i start calego stacku

```bash
cd /opt/investio
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec api python -m alembic upgrade head
```

## Krok 6: WordPress

Otworz `https://blog.{DOMAIN_PUNYCODE}` - przejdz przez instalator,
ustaw permalinki na "Nazwa wpisu", opublikuj testowy wpis.

## Krok 7: Weryfikacja

- https://{DOMAIN_PUNYCODE} - frontend
- https://api.{DOMAIN_PUNYCODE}/docs - API
- https://blog.{DOMAIN_PUNYCODE} - WordPress

## Aktualizacje (po zmianach w kodzie)

```bash
cd /opt/investio
git pull   # albo ponownie scp
docker compose -f docker-compose.prod.yml build web api worker
docker compose -f docker-compose.prod.yml up -d
```
'''


def main() -> None:
    if not os.path.exists("docker-compose.yml"):
        print("UWAGA: nie widze docker-compose.yml w tym katalogu.")
        print("Upewnij sie, ze uruchamiasz skrypt wewnatrz folderu mvp-portal-projektow.")
        return

    for rel_path, content in FILES.items():
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  napisano: {rel_path}")

    print("\\nGotowe. Otworz DEPLOYMENT.md i postepuj krok po kroku.")
    print("Zacznij od DNS (Krok 0) - bez tego certyfikaty SSL nie przejda.")


if __name__ == "__main__":
    main()
