#!/usr/bin/env python3
"""
Podmienia tekstowy naglowek "Portal Projektow" na logo graficzne
(Investio) w frontend/src/app/layout.tsx.

WAZNE - krok reczny przed uruchomieniem skryptu:
  1. Zapisz plik z logo (ten, ktory wygenerowalismy/przeslalismy w
     czacie) jako:
         mvp-portal-projektow/frontend/public/logo.png
     (Next.js automatycznie serwuje wszystko z folderu "public" pod
     adresem "/", wiec logo bedzie dostepne pod /logo.png)

  2. Jesli folder "public" jeszcze nie istnieje w frontend/, po
     prostu go utworz i wloz tam plik logo.png.

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 add_logo.py

Po uruchomieniu:
    docker compose up -d --build web
    otworz http://localhost:3001 i odswiez (Ctrl+Shift+R)
"""
import os

FILES: dict[str, str] = {}

FILES["frontend/src/app/layout.tsx"] = '''import "./globals.css";
import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";

export const metadata = {
  title: "Investio",
  description: "Katalog i weryfikacja projektow inwestycyjnych",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pl">
      <body className="bg-gray-50 text-gray-900">
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
            <Link href="/" className="flex items-center">
              <Image
                src="/logo.png"
                alt="Investio"
                width={160}
                height={40}
                priority
                className="h-8 w-auto"
              />
            </Link>
            <nav className="flex gap-4 text-sm">
              <a href="/projekty">Projekty</a>
              <a href="/blog">Blog</a>
              <a href="/faq">FAQ</a>
              <a href="/jak-to-dziala">Jak to dziala</a>
              <a href="/ryzyka">Ryzyka</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="border-t mt-16 py-6 text-center text-sm text-gray-500">
          Ta platforma nie przyjmuje platnosci, wplat ani inwestycji. Deklaracje zainteresowania
          nie sa zobowiazaniem finansowym.
        </footer>
      </body>
    </html>
  );
}
'''


def main() -> None:
    if not os.path.exists("docker-compose.yml"):
        print("UWAGA: nie widze docker-compose.yml w tym katalogu.")
        print("Upewnij sie, ze uruchamiasz skrypt wewnatrz folderu mvp-portal-projektow.")
        return

    logo_path = os.path.join("frontend", "public", "logo.png")
    os.makedirs(os.path.dirname(logo_path), exist_ok=True)

    if not os.path.exists(logo_path):
        print("UWAGA: nie znaleziono pliku frontend/public/logo.png")
        print("Zapisz tam plik z logo PRZED odswiezeniem strony (patrz docstring skryptu).")
        print("Kontynuuje aktualizacje layout.tsx - logo dodasz w dowolnym momencie pozniej.\\n")

    created = 0
    for rel_path, content in FILES.items():
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"  napisano: {rel_path}")

    print(f"\\nZaktualizowano {created} plikow.")
    print("\\nNastepne kroki:")
    print("  1. upewnij sie, ze plik logo jest zapisany jako:")
    print("     frontend/public/logo.png")
    print("  2. docker compose up -d --build web")
    print("  3. otworz http://localhost:3001 (Ctrl+Shift+R dla pewnosci)")


if __name__ == "__main__":
    main()
