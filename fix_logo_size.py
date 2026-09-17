#!/usr/bin/env python3
"""
Zwieksza rozmiar logo w headerze i koryguje kontener, tak aby
kompensowac biale marginesy w samym pliku logo.png.

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 fix_logo_size.py
    docker compose up -d --build web
    otworz http://localhost:3001 (Ctrl+Shift+R)

Jesli logo WCIAZ wyglada malo (bo w pliku PNG/JPG jest duzo pustego
tla wokol napisu), najlepszym rozwiazaniem jest przyciecie obrazka
(crop) w edytorze graficznym tak, by tekst "investio" wypelnial caly
kadr - wtedy nawet mala wysokosc kontenera bedzie wygladac dobrze.
Ten skrypt jednak w miedzyczasie znaczaco zwieksza wysokosc
kontenera, co powinno pomoc nawet bez przycinania.
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
          <div className="mx-auto max-w-6xl px-4 py-2 flex items-center justify-between">
            <Link href="/" className="flex items-center shrink-0">
              <Image
                src="/logo.png"
                alt="Investio"
                width={400}
                height={100}
                priority
                className="h-16 w-auto object-contain"
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

    for rel_path, content in FILES.items():
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  napisano: {rel_path}")

    print("\\nNastepne kroki:")
    print("  docker compose up -d --build web")
    print("  otworz http://localhost:3001 (Ctrl+Shift+R)")
    print("\\nJesli logo wciaz jest za male, przycinij biale marginesy")
    print("w samym pliku logo.png (edytor graficzny / narzedzie do crop)")
    print("tak, by napis 'investio' wypelnial caly kadr obrazka.")


if __name__ == "__main__":
    main()
