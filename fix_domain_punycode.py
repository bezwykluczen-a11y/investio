#!/usr/bin/env python3
"""
Poprawia punycode domeny we wszystkich plikach produkcyjnych.

Stara (bledna) wartosc: xn--spki-niemieckie-xrb.pl
Nowa (poprawna):        xn--spki-niemieckie-wrb75k.pl

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 fix_domain_punycode.py
"""
import os

OLD = "xn--spki-niemieckie-xrb.pl"
NEW = "xn--spki-niemieckie-wrb75k.pl"

TARGET_FILES = [
    "docker-compose.prod.yml",
    "backend/.env.production.example",
    "infra/nginx/spolki-niemieckie.conf",
    "infra/nginx/api.spolki-niemieckie.conf",
    "infra/nginx/blog.spolki-niemieckie.conf",
    "DEPLOYMENT.md",
]


def main() -> None:
    if not os.path.exists("docker-compose.prod.yml"):
        print("UWAGA: nie widze docker-compose.prod.yml w tym katalogu.")
        print("Najpierw uruchom: python prepare_production_v2.py")
        return

    total_replacements = 0
    for rel_path in TARGET_FILES:
        if not os.path.exists(rel_path):
            print(f"  POMINIETO (brak pliku): {rel_path}")
            continue
        with open(rel_path, "r", encoding="utf-8") as f:
            content = f.read()
        count = content.count(OLD)
        if count == 0:
            print(f"  bez zmian: {rel_path}")
            continue
        content = content.replace(OLD, NEW)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        total_replacements += count
        print(f"  poprawiono ({count}x): {rel_path}")

    print(f"\\nLacznie podmieniono {total_replacements} wystapien.")
    print(f"Nowa domena: {NEW}")
    print("\\nNastepny krok: rekordy DNS w DirectAdmin (cyber-Folks):")
    print("  A  @     -> 77.42.64.51")
    print("  A  www   -> 77.42.64.51")
    print("  A  api   -> 77.42.64.51")
    print("  A  blog  -> 77.42.64.51")


if __name__ == "__main__":
    main()
