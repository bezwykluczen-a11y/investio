#!/usr/bin/env python3
"""
Dodaje logowanie, rejestracje i panel uzytkownika do frontendu Next.js.

Backend juz ma endpointy /api/v1/auth/login i /api/v1/auth/register,
ktore zwracaja JWT. Ten skrypt tworzy:

  1. frontend/src/lib/auth.ts          - funkcje login/register/logout + obsluga tokenu
  2. frontend/src/app/logowanie/page.tsx  - formularz logowania
  3. frontend/src/app/rejestracja/page.tsx - formularz rejestracji
  4. frontend/src/app/konto/page.tsx      - panel uzytkownika (chroniony)
  5. frontend/src/app/konto/obserwowane/page.tsx - watchlist
  6. frontend/src/components/ProtectedRoute.tsx - komponent chroniacy trasy
  7. frontend/src/components/AuthNav.tsx  - linki login/logout w headerze (dynamiczne)
  8. frontend/src/app/layout.tsx          - zaktualizowany z AuthNav

Token JWT jest przechowywany w localStorage (rozwiazanie MVP - docelowo
nalezy go przeniesc do HttpOnly cookie, co opisze w komentarzach).

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 add_auth_user_panel.py

Po uruchomieniu:
    docker compose up -d --build web
    otworz http://localhost:3001/logowanie
"""
import os

FILES: dict[str, str] = {}

FILES["frontend/src/lib/auth.ts"] = '''const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const TOKEN_KEY = "investio_access_token";

export type LoginPayload = { email: string; password: string };
export type RegisterPayload = { email: string; password: string; full_name: string };
export type TokenResponse = { access_token: string; token_type: string };

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function removeToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function isLoggedIn(): boolean {
  return !!getToken();
}

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "Nieprawidlowy email lub haslo");
  }
  const data: TokenResponse = await res.json();
  setToken(data.access_token);
  return data;
}

export async function register(payload: RegisterPayload): Promise<void> {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "Blad rejestracji");
  }
}

export function logout(): void {
  removeToken();
  window.location.href = "/";
}

export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function decodeJwtPayload(token: string): Record<string, unknown> | null {
  try {
    const payload = token.split(".")[1];
    const decoded = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decodeURIComponent(escape(decoded)));
  } catch {
    return null;
  }
}

export function getUserEmailFromToken(): string | null {
  const token = getToken();
  if (!token) return null;
  const payload = decodeJwtPayload(token);
  return payload?.sub as string | null;
}
'''

FILES["frontend/src/components/AuthNav.tsx"] = '''"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { isLoggedIn, logout, getUserEmailFromToken } from "@/lib/auth";

export function AuthNav() {
  const [mounted, setMounted] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    setMounted(true);
    setLoggedIn(isLoggedIn());
    setEmail(getUserEmailFromToken());
  }, []);

  if (!mounted) return null;

  if (!loggedIn) {
    return (
      <>
        <Link href="/logowanie" className="hover:text-gray-700">
          Logowanie
        </Link>
        <Link href="/rejestracja" className="hover:text-gray-700">
          Rejestracja
        </Link>
      </>
    );
  }

  return (
    <>
      <Link href="/konto" className="hover:text-gray-700">
        Moje konto
      </Link>
      <span className="text-gray-500 text-xs hidden sm:inline">{email}</span>
      <button
        onClick={logout}
        className="text-sm text-red-600 hover:text-red-800"
      >
        Wyloguj
      </button>
    </>
  );
}
'''

FILES["frontend/src/components/ProtectedRoute.tsx"] = '''"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { isLoggedIn } from "@/lib/auth";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/logowanie");
    }
  }, [router]);

  if (typeof window !== "undefined" && !isLoggedIn()) {
    return null;
  }

  return <>{children}</>;
}
'''

FILES["frontend/src/app/logowanie/page.tsx"] = '''"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login({ email, password });
      router.push("/konto");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Blad logowania");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Logowanie</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Adres e-mail
          </label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            placeholder="twoj@email.pl"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Haslo
          </label>
          <input
            id="password"
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            placeholder="••••••••"
          />
        </div>

        {error && (
          <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? "Logowanie..." : "Zaloguj sie"}
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-gray-600">
        Nie masz konta?{" "}
        <Link href="/rejestracja" className="text-gray-900 underline">
          Zarejestruj sie
        </Link>
      </p>
    </div>
  );
}
'''

FILES["frontend/src/app/rejestracja/page.tsx"] = '''"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { register, login } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Hasla nie sa identyczne");
      return;
    }
    if (password.length < 8) {
      setError("Haslo musi miec co najmniej 8 znakow");
      return;
    }

    setLoading(true);
    try {
      await register({ full_name: fullName, email, password });
      await login({ email, password });
      router.push("/konto");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Blad rejestracji");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Rejestracja</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-1">
            Imie i nazwisko
          </label>
          <input
            id="fullName"
            type="text"
            required
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            placeholder="Jan Kowalski"
          />
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Adres e-mail
          </label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            placeholder="twoj@email.pl"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Haslo
          </label>
          <input
            id="password"
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            placeholder="••••••••"
          />
        </div>

        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
            Powtorz haslo
          </label>
          <input
            id="confirmPassword"
            type="password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            placeholder="••••••••"
          />
        </div>

        {error && (
          <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? "Rejestracja..." : "Zarejestruj sie"}
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-gray-600">
        Masz juz konto?{" "}
        <Link href="/logowanie" className="text-gray-900 underline">
          Zaloguj sie
        </Link>
      </p>
    </div>
  );
}
'''

FILES["frontend/src/app/konto/page.tsx"] = '''"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import Link from "next/link";
import { getUserEmailFromToken } from "@/lib/auth";
import { useEffect, useState } from "react";

function KontoContent() {
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    setEmail(getUserEmailFromToken());
  }, []);

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Moje konto</h1>
        {email && (
          <p className="text-sm text-gray-500 mt-1">Zalogowany jako: {email}</p>
        )}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Link
          href="/konto/obserwowane"
          className="block rounded-lg border bg-white p-5 hover:shadow-md transition-shadow"
        >
          <h2 className="font-semibold text-lg">Obserwowane projekty</h2>
          <p className="mt-2 text-sm text-gray-600">
            Lista projektow, ktore obserwujesz
          </p>
        </Link>

        <Link
          href="/konto/deklaracje"
          className="block rounded-lg border bg-white p-5 hover:shadow-md transition-shadow"
        >
          <h2 className="font-semibold text-lg">Deklaracje zainteresowania</h2>
          <p className="mt-2 text-sm text-gray-600">
            Twoje zgloszenia zainteresowania projektami
          </p>
        </Link>

        <Link
          href="/konto/pytania"
          className="block rounded-lg border bg-white p-5 hover:shadow-md transition-shadow"
        >
          <h2 className="font-semibold text-lg">Moje pytania</h2>
          <p className="mt-2 text-sm text-gray-600">
            Pytania, ktore zadales do projektow
          </p>
        </Link>

        <Link
          href="/konto/ustawienia"
          className="block rounded-lg border bg-white p-5 hover:shadow-md transition-shadow"
        >
          <h2 className="font-semibold text-lg">Ustawienia</h2>
          <p className="mt-2 text-sm text-gray-600">
            Zmiana hasla, powiadomienia, profil
          </p>
        </Link>
      </div>
    </div>
  );
}

export default function KontoPage() {
  return (
    <ProtectedRoute>
      <KontoContent />
    </ProtectedRoute>
  );
}
'''

FILES["frontend/src/app/konto/obserwowane/page.tsx"] = '''"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

type WatchlistItem = {
  id: string;
  project: {
    id: string;
    title: string;
    slug: string;
    short_description: string;
    category: string;
    location_general: string | null;
  };
};

function ObserwowaneContent() {
  const [items, setItems] = useState<WatchlistItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchWatchlist() {
      const token = getToken();
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API_URL}/me/watchlist`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
          const data = await res.json();
          setItems(data);
        }
      } catch {
        // blad sieci - pokazemy pusta liste
      } finally {
        setLoading(false);
      }
    }
    fetchWatchlist();
  }, []);

  if (loading) return <p className="text-gray-500">Ladowanie...</p>;

  if (items.length === 0) {
    return (
      <div className="space-y-4">
        <h1 className="text-2xl font-bold">Obserwowane projekty</h1>
        <p className="text-gray-600">
          Nie obserwujesz jeszcze zadnych projektow. Przegladaj{" "}
          <a href="/projekty" className="underline">katalog projektow</a>{" "}
          i kliknij "Obserwuj" przy interesujacym projekcie.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Obserwowane projekty</h1>
      <div className="grid gap-4 sm:grid-cols-2">
        {items.map((item) => (
          <a
            key={item.id}
            href={`/projekty/${item.project.slug}`}
            className="block rounded-lg border bg-white p-4 hover:shadow-md transition-shadow"
          >
            <h3 className="font-semibold">{item.project.title}</h3>
            <p className="mt-1 text-sm text-gray-600 line-clamp-2">
              {item.project.short_description}
            </p>
            {item.project.location_general && (
              <p className="mt-2 text-xs text-gray-500">{item.project.location_general}</p>
            )}
          </a>
        ))}
      </div>
    </div>
  );
}

export default function ObserwowanePage() {
  return (
    <ProtectedRoute>
      <ObserwowaneContent />
    </ProtectedRoute>
  );
}
'''

FILES["frontend/src/app/layout.tsx"] = '''import "./globals.css";
import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import { AuthNav } from "@/components/AuthNav";

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
        <footer className="border-t mt-16 py-6 text-center text-sm text-gray-500">
          <div className="space-y-2">
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

    created = 0
    for rel_path, content in FILES.items():
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"  napisano: {rel_path}")

    print(f"\\nZaktualizowano/dodano {created} plikow.")
    print("\\nNastepne kroki:")
    print("  docker compose up -d --build web")
    print("  otworz http://localhost:3001/logowanie")
    print("  zaloguj sie kontem utworzonym wczesniej w /docs (admin@test.pl)")
    print("\\nUWAGA: panel /konto/deklaracje, /konto/pytania, /konto/ustawienia")
    print("sa na razie placeholderami (linki istnieja, strony do dobudowania).")


if __name__ == "__main__":
    main()
