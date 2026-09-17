# Deployment na Hetzner - spolki-niemieckie.pl (v2)

Domena (punycode): `xn--spki-niemieckie-wrb75k.pl`
Serwer: `77.42.64.51`

WAZNE: na serwerze juz dziala systemowy nginx (seomasters.com.pl itd.).
NIE odpalamy nginx w Dockerze - kontenery wystawiamy na 127.0.0.1,
a systemowy nginx robi proxy.

## Krok 0: DNS

W panelu domeny dodaj rekordy A -> 77.42.64.51: `@`, `www`, `api`, `blog`.
Sprawdz: `nslookup api.xn--spki-niemieckie-wrb75k.pl`.

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
certbot --nginx -d xn--spki-niemieckie-wrb75k.pl -d www.xn--spki-niemieckie-wrb75k.pl
certbot --nginx -d api.xn--spki-niemieckie-wrb75k.pl
certbot --nginx -d blog.xn--spki-niemieckie-wrb75k.pl
```

Certbot sam przepisze konfigi na HTTPS i doda redirect z HTTP.

## Krok 7: WordPress

Otworz `https://blog.xn--spki-niemieckie-wrb75k.pl` - instalator, permalinki
na "Nazwa wpisu", testowy wpis.

## Krok 8: Weryfikacja

- https://xn--spki-niemieckie-wrb75k.pl (czyli https://spolki-niemieckie.pl)
- https://api.xn--spki-niemieckie-wrb75k.pl/docs
- https://blog.xn--spki-niemieckie-wrb75k.pl

## Aktualizacje

```bash
cd /opt/investio
# (wgraj nowy kod: scp/git)
docker compose -f docker-compose.prod.yml build web api worker
docker compose -f docker-compose.prod.yml up -d
```
