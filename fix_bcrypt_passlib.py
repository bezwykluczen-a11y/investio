#!/usr/bin/env python3
"""
Naprawia konflikt passlib + bcrypt 5.x w backendzie.

Problem: passlib 1.7.4 podczas inicjalizacji bcrypt wykonuje test
wewnetrzny z haslem >72 bajtow, co w bcrypt 5.x rzuca ValueError
zamiast cicho ucinac. Efekt: 500 Internal Server Error przy
rejestracji/logowaniu.

Rozwiazanie: przypinamy bcrypt do wersji 4.1.3 (kompatybilna z passlib)
w requirements.txt i przebudowujemy obraz api/worker.

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 fix_bcrypt_passlib.py
    docker compose up -d --build api worker

Po przebudowaniu:
    otworz http://localhost:8000/docs i przetestuj POST /api/v1/auth/register
"""
import os

FILES: dict[str, str] = {}

FILES["backend/requirements.txt"] = """fastapi==0.111.0
uvicorn[standard]==0.30.1
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.3
python-multipart==0.0.9
email-validator==2.1.1
redis==5.0.4
celery==5.4.0
boto3==1.34.100
python-slugify==8.0.4
"""


def main() -> None:
    if not os.path.exists("docker-compose.yml"):
        print("UWAGA: nie widze docker-compose.yml w tym katalogu.")
        print("Upewnij sie, ze uruchamiasz skrypt wewnatrz folderu mvp-portal-projektow.")
        return

    for rel_path, content in FILES.items():
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  napisano: {rel_path}")

    print("\\nNastepne kroki:")
    print("  docker compose up -d --build api worker")
    print("  (to przebuduje obrazy z poprawiona wersja bcrypt)")
    print("\\nPo przebudowaniu:")
    print("  otworz http://localhost:8000/docs")
    print("  przetestuj POST /api/v1/auth/register")


if __name__ == "__main__":
    main()
