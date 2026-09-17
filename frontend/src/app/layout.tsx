import "./globals.css";
import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import { AuthNav } from "@/components/AuthNav";

export const metadata = {
  title: "Investio - łączymy kapitał z dobrymi projektami",
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
            <nav className="flex gap-4 text-sm items-center">
              <a href="/projekty">Projekty</a>
              <a href="/blog">Blog</a>
              <a href="/faq">FAQ</a>
              <a href="/jak-to-dziala">Jak to dziala</a>
              <a href="/ryzyka">Ryzyka</a>
              <AuthNav />
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="border-t mt-16 py-8 text-sm text-gray-500">
          <div className="mx-auto max-w-6xl px-4 flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
            <div className="flex items-start gap-3">
              <Image
                src="/logo.png"
                alt="Investio"
                width={160}
                height={40}
                className="h-10 w-auto object-contain shrink-0"
              />
              <div className="text-xs leading-relaxed text-gray-500">
                <p className="font-medium text-gray-700">
                  ELLUS CENTRUM BADAWCZO ROZWOJOWE SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA
                </p>
                <p>Aleje Jerozolimskie 85 / 21, 02-001 Warszawa, Polska</p>
                <p>NIP: 7011221932</p>
              </div>
            </div>
            <div className="space-y-2 text-center sm:text-right">
              <p>
                Ta platforma nie przyjmuje platnosci, wplat ani inwestycji.
                Deklaracje zainteresowania nie sa zobowiazaniem finansowym.
              </p>
              <p>
                <a href="/polityka-prywatnosci" className="underline hover:text-gray-700">
                  Polityka prywatnosci
                </a>
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
