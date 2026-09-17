#!/usr/bin/env python3
"""
Przygotowuje pliki produkcyjne v2 dla deploymentu na Hetzner.
Dostosowane do serwera, na ktorym JUZ dziala systemowy nginx
(porty 80/443 zajete przez nginx systemowy, nie kontenerowy).

Architektura:
  - kontenery Dockera wystawione na 127.0.0.1 (3000, 8000, 8081)
  - systemowy nginx proxy-passes do nich
  - SSL przez systemowy certbot

Tworzy:
  - docker-compose.prod.yml          (bez nginx/certbot w srodku)
  - frontend/Dockerfile.prod
  - backend/.env.production.example
  - infra/nginx/spolki-niemieckie.conf      (do /etc/nginx/sites-available/)
  - infra/nginx/api.spolki-niemieckie.conf
  - infra/nginx/blog.spolki-niemieckie.conf
  - DEPLOYMENT.md                    (zaktualizowana instrukcja)

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 prepare_production_v2.py
"""
import os

DOMAIN_PUNYCODE = "xn--spki-niemieckie-xrb.pl"

FILES: dict[str, str] = {}

FILES["docker-compose.prod.yml"] = '''services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: portal
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
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
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
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
    ports:
      - "127.0.0.1:8000:8000"

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
        NEXT_PUBLIC_API_URL: https://api.xn--spki-niemieckie-xrb.pl/api/v1
        WORDPRESS_API_URL: https://blog.xn--spki-niemieckie-xrb.pl/wp-json/wp/v2
    restart: unless-stopped
    depends_on:
      - api
      - wordpress
    ports:
      - "127.0.0.1:3000:3000"

  wordpress-db:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: ${WORDPRESS_DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${WORDPRESS_DB_ROOT_PASSWORD}
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
      WORDPRESS_DB_PASSWORD: ${WORDPRESS_DB_PASSWORD}
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_CONFIG_EXTRA: |
        define('WP_HOME', 'https://blog.xn--spki-niemieckie-xrb.pl');
        define('WP_SITEURL', 'https://blog.xn--spki-niemieckie-xrb.pl');
        if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
            $_SERVER['HTTPS'] = 'on';
        }
    depends_on:
      - wordpress-db
    volumes:
      - wordpress_data:/var/www/html
    ports:
      - "127.0.0.1:8081:80"

volumes:
  db_data:
  minio_data:
  wordpress_data:
  wordpress_db_data:
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

FILES["backend/.env.production.example"] = '''ENVIRONMENT=production
SECRET_KEY=UZUPELNIC-losowy-64-znakowy-ciag
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+psycopg2://portal:UZUPELNIC-haslo-db@db:5432/portal
REDIS_URL=redis://redis:6379/0
CORS_ORIGINS=https://xn--spki-niemieckie-xrb.pl,https://www.xn--spki-niemieckie-xrb.pl
STORAGE_BUCKET=portal-documents
STORAGE_ENDPOINT_URL=http://minio:9000
STORAGE_ACCESS_KEY=UZUPELNIC
STORAGE_SECRET_KEY=UZUPELNIC
MAX_UPLOAD_MB=15
'''

FILES["infra/nginx/spolki-niemieckie.conf"] = '''# Frontend (Next.js) - domena glowna
# Wgraj do: /etc/nginx/sites-available/spolki-niemieckie.conf
# potem: ln -s /etc/nginx/sites-available/spolki-niemieckie.conf /etc/nginx/sites-enabled/

server {
    listen 80;
    server_name xn--spki-niemieckie-xrb.pl www.xn--spki-niemieckie-xrb.pl;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
'''

FILES["infra/nginx/api.spolki-niemieckie.conf"] = '''# Backend (FastAPI) - subdomena api
# Wgraj do: /etc/nginx/sites-available/api.spolki-niemieckie.conf

server {
    listen 80;
    server_name api.xn--spki-niemieckie-xrb.pl;

    client_max_body_size 20m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
'''

FILES["infra/nginx/blog.spolki-niemieckie.conf"] = '''# WordPress (blog headless) - subdomena blog
# Wgraj do: /etc/nginx/sites-available/blog.spolki-niemieckie.conf

server {
    listen 80;
    server_name blog.xn--spki-niemieckie-xrb.pl;

    client_max_body_size 20m;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
'''

FILES["DEPLOYMENT.md"] = '''# Deployment na Hetzner - spolki-niemieckie.pl (v2)

Domena (punycode): `xn--spki-niemieckie-xrb.pl`
Serwer: `77.42.64.51`

WAZNE: na serwerze juz dziala systemowy nginx (seomasters.com.pl itd.).
NIE odpalamy nginx w Dockerze - kontenery wystawiamy na 127.0.0.1,
a systemowy nginx robi proxy.

## Krok 0: DNS

W panelu domeny dodaj rekordy A -> 77.42.64.51: `@`, `www`, `api`, `blog`.
Sprawdz: `nslookup api.xn--spki-niemieckie-xrb.pl`.

## Krok 1: Docker na serwerze

```bash
ssh root@77.42.64.51
apt update && apt upgrade -y
curl -fsSL https://get.docker.com | sh
apt install -y docker-compose-plugin
docker ps
```

## Krok 2: Wgranie kodu

Lokalnie (PowerShell, w folderze projektu):

```powershell
tar -czf investio.tar.gz --exclude=node_modules --exclude=.next --exclude=__pycache__ .
scp investio.tar.gz root@77.42.64.51:/root/
```

Na serwerze:

```bash
mkdir -p /opt/investio
cd /opt/investio
tar -xzf /root/investio.tar.gz
```

## Krok 3: Konfiguracja

```bash
cd /opt/investio
cp backend/.env.production.example backend/.env.production
openssl rand -hex 32   # wklej jako SECRET_KEY
nano backend/.env.production
```

Plik z haslami (w katalogu z docker-compose.prod.yml):

```bash
nano /opt/investio/.env
```

```
POSTGRES_PASSWORD=...losowe...
MINIO_ROOT_USER=investio
MINIO_ROOT_PASSWORD=...losowe...
WORDPRESS_DB_PASSWORD=...losowe...
WORDPRESS_DB_ROOT_PASSWORD=...losowe...
```

## Krok 4: Konfiguracja systemowego nginx

```bash
cp /opt/investio/infra/nginx/spolki-niemieckie.conf /etc/nginx/sites-available/
cp /opt/investio/infra/nginx/api.spolki-niemieckie.conf /etc/nginx/sites-available/
cp /opt/investio/infra/nginx/blog.spolki-niemieckie.conf /etc/nginx/sites-available/

ln -s /etc/nginx/sites-available/spolki-niemieckie.conf /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/api.spolki-niemieckie.conf /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/blog.spolki-niemieckie.conf /etc/nginx/sites-enabled/

nginx -t
systemctl reload nginx
```

## Krok 5: Build i start stacku

```bash
cd /opt/investio
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec api python -m alembic upgrade head
```

Sprawdz: `docker compose -f docker-compose.prod.yml ps` - wszystko powinno byc Up.

## Krok 6: SSL (certbot systemowy)

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d xn--spki-niemieckie-xrb.pl -d www.xn--spki-niemieckie-xrb.pl
certbot --nginx -d api.xn--spki-niemieckie-xrb.pl
certbot --nginx -d blog.xn--spki-niemieckie-xrb.pl
```

Certbot sam przepisze konfigi na HTTPS i doda redirect z HTTP.

## Krok 7: WordPress

Otworz `https://blog.xn--spki-niemieckie-xrb.pl` - instalator, permalinki
na "Nazwa wpisu", testowy wpis.

## Krok 8: Weryfikacja

- https://xn--spki-niemieckie-xrb.pl (czyli https://spolki-niemieckie.pl)
- https://api.xn--spki-niemieckie-xrb.pl/docs
- https://blog.xn--spki-niemieckie-xrb.pl

## Aktualizacje

```bash
cd /opt/investio
# (wgraj nowy kod: scp/git)
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
    print("Kolejnosc: DNS -> Docker na serwerze -> wgranie kodu -> nginx -> build -> SSL.")


if __name__ == "__main__":
    main()
