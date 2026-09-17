"use client";

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
