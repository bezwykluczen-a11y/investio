"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import Link from "next/link";
import { getUserEmailFromToken, getUserRoleFromToken } from "@/lib/auth";
import { useEffect, useState } from "react";

function KontoContent() {
  const [email, setEmail] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    setEmail(getUserEmailFromToken());
    setRole(getUserRoleFromToken());
  }, []);

  const isModeratorOrAdmin = role === "moderator" || role === "admin";

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

        {isModeratorOrAdmin && (
          <>
            <Link
              href="/panel/organizacje"
              className="block rounded-lg border-2 border-black bg-white p-5 hover:shadow-md transition-shadow"
            >
              <h2 className="font-semibold text-lg">Organizacje</h2>
              <p className="mt-2 text-sm text-gray-600">
                Zarzadzaj organizacjami i dodawaj do nich projekty
              </p>
            </Link>

            <Link
              href="/panel/nowy-projekt"
              className="block rounded-lg border-2 border-black bg-white p-5 hover:shadow-md transition-shadow"
            >
              <h2 className="font-semibold text-lg">Nowy projekt</h2>
              <p className="mt-2 text-sm text-gray-600">
                Dodaj nowy projekt inwestycyjny
              </p>
            </Link>

            <Link
              href="/panel/projekty"
              className="block rounded-lg border-2 border-black bg-white p-5 hover:shadow-md transition-shadow"
            >
              <h2 className="font-semibold text-lg">Wszystkie projekty</h2>
              <p className="mt-2 text-sm text-gray-600">
                Przegladaj i usuwaj istniejace projekty
              </p>
            </Link>
          </>
        )}
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
