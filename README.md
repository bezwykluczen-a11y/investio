# Portal Projektow - MVP (bez platnosci)

MVP portalu do katalogowania i weryfikacji projektow inwestycyjnych (osiedla,
biogazownie, strzelnice itd.). Wersja nie obsluguje platnosci, wplat ani
inwestycji - to katalog + system weryfikacji dokumentow + deklaracje
zainteresowania.

## Struktura repo

```
backend/     FastAPI + SQLAlchemy + Alembic
frontend/    Next.js (App Router) + Tailwind
infra/       Dockerfile, docker-compose
```

## Szybki start (lokalnie, Docker)

1. Skopiuj `.env`:
   ```
   cp backend/.env.example backend/.env
   ```
   Ustaw wlasny `SECRET_KEY` (np. `openssl rand -hex 32`).

2. Uruchom caly stack:
   ```
   docker compose up --build
   ```

3. Wykonaj migracje bazy (w kontenerze `api`):
   ```
   docker compose exec api alembic upgrade head
   ```

4. Adresy:
   - API: http://localhost:8000/api/v1 (docs: http://localhost:8000/docs)
   - Frontend: http://localhost:3000
   - MinIO console: http://localhost:9001 (minioadmin / minioadmin)

## Bez Dockera (backend)

```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# ustaw DATABASE_URL na lokalny Postgres
alembic upgrade head
uvicorn app.main:app --reload
```

## Bez Dockera (frontend)

```
cd frontend
npm install
npm run dev
```

## Pierwsze kroki po uruchomieniu

1. `POST /api/v1/auth/register` - zaloz konto.
2. `POST /api/v1/auth/login` - zaloguj sie, odbierz token JWT.
3. `POST /api/v1/organizations` - zaloz organizacje (Bearer token).
4. `POST /api/v1/projects/organizations/{organization_id}` - dodaj projekt (status `draft`).
5. `POST /api/v1/projects/{project_id}/submit` - zglos projekt do weryfikacji.
6. Recznie w bazie nadaj sobie role `admin` lub `analyst`, aby zmieniac statusy
   przez `POST /api/v1/projects/{project_id}/status`.
7. Po ustawieniu statusu `published` projekt pojawi sie w `/projekty` na
   frontendzie.

## Co jest w zakresie MVP

- Rejestracja/logowanie (JWT), RBAC (user/organizer/analyst/moderator/admin).
- Organizacje i czlonkostwa.
- Projekty ze statusami (draft -> submitted -> in_review -> verified ->
  published, + needs_changes/paused/completed/rejected).
- Publiczny katalog i karta projektu.
- Pytania do projektu, watchlist, deklaracje zainteresowania (NIE platnosci).
- Dziennik audytowy zmian statusow.
- Panel admina (lista projektow, audit log) - API gotowe, UI do dobudowania.

## Czego NIE ma (celowo)

- Platnosci, wplat, wyplat, integracji z operatorem platniczym.
- Emisji udzialow/akcji, umow pozyczki.
- Automatycznej oceny inwestora / rekomendacji finansowych.

## Nastepne kroki

1. Upload dokumentow (S3/MinIO) + skanowanie plikow (worker Celery - szkielet
   juz jest w `app/worker.py`).
2. UI panelu pomyslodawcy i panelu admina (frontend).
3. MFA dla rol analyst/moderator/admin.
4. Testy (pytest) dla przejsc statusow i RBAC.
5. CI/CD + monitoring (Sentry/Prometheus).
