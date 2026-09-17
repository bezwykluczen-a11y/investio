"use client";

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
