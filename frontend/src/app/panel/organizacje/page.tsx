"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getMyOrganizations, createOrganization, Organization } from "@/lib/api";

function OrganizacjeContent() {
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const [name, setName] = useState("");
  const [legalName, setLegalName] = useState("");
  const [nip, setNip] = useState("");
  const [krs, setKrs] = useState("");
  const [description, setDescription] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadOrgs() {
    setLoading(true);
    const data = await getMyOrganizations();
    setOrgs(data);
    setLoading(false);
  }

  useEffect(() => {
    loadOrgs();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await createOrganization({
        name,
        legal_name: legalName || undefined,
        nip: nip || undefined,
        krs: krs || undefined,
        description: description || undefined,
      });
      setName("");
      setLegalName("");
      setNip("");
      setKrs("");
      setDescription("");
      setShowForm(false);
      await loadOrgs();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Wystapil blad");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Organizacje</h1>
          <p className="mt-1 text-sm text-gray-500">
            Organizacje, w ktorych mozesz zarzadzac projektami
          </p>
        </div>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
        >
          {showForm ? "Anuluj" : "Nowa organizacja"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="rounded-lg border bg-white p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nazwa organizacji *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              minLength={2}
              maxLength={255}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Nazwa prawna (opcjonalnie)</label>
            <input
              type="text"
              value={legalName}
              onChange={(e) => setLegalName(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">NIP (opcjonalnie)</label>
              <input
                type="text"
                value={nip}
                onChange={(e) => setNip(e.target.value)}
                maxLength={20}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">KRS (opcjonalnie)</label>
              <input
                type="text"
                value={krs}
                onChange={(e) => setKrs(e.target.value)}
                maxLength={20}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Opis (opcjonalnie)</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          <button
            type="submit"
            disabled={saving}
            className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
          >
            {saving ? "Zapisywanie..." : "Utworz organizacje"}
          </button>
        </form>
      )}

      {loading ? (
        <p className="text-gray-500">Ladowanie...</p>
      ) : orgs.length === 0 ? (
        <p className="text-gray-600">Nie masz jeszcze zadnej organizacji.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {orgs.map((org) => (
            <div key={org.id} className="rounded-lg border bg-white p-5">
              <h3 className="font-semibold">{org.name}</h3>
              {org.legal_name && <p className="mt-1 text-sm text-gray-600">{org.legal_name}</p>}
              <p className="mt-2 text-xs text-gray-400">
                {org.is_verified ? "Zweryfikowana" : "Niezweryfikowana"}
              </p>
              <Link
                href={`/panel/nowy-projekt?organization_id=${org.id}`}
                className="mt-3 inline-block text-sm font-medium underline"
              >
                Dodaj projekt w tej organizacji
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function OrganizacjePage() {
  return (
    <ProtectedRoute allowedRoles={["moderator", "admin"]}>
      <OrganizacjeContent />
    </ProtectedRoute>
  );
}
