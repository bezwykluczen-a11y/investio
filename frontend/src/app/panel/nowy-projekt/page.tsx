"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { getMyOrganizations, createProject, Organization, ProjectDetail } from "@/lib/api";

const CATEGORIES: { value: string; label: string }[] = [
  { value: "housing", label: "Budownictwo mieszkaniowe" },
  { value: "energy_biogas", label: "Energetyka i biogaz" },
  { value: "local_infrastructure", label: "Infrastruktura lokalna" },
  { value: "sports_recreation", label: "Sport i rekreacja" },
  { value: "industrial", label: "Przemysl" },
  { value: "municipal", label: "Projekty gminne" },
  { value: "other", label: "Inne" },
];

function NowyProjektContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const preselectedOrgId = searchParams.get("organization_id") || "";

  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [loadingOrgs, setLoadingOrgs] = useState(true);
  const [organizationId, setOrganizationId] = useState(preselectedOrgId);

  const [title, setTitle] = useState("");
  const [shortDescription, setShortDescription] = useState("");
  const [fullDescription, setFullDescription] = useState("");
  const [category, setCategory] = useState("housing");
  const [voivodeship, setVoivodeship] = useState("");
  const [locationGeneral, setLocationGeneral] = useState("");
  const [estimatedBudget, setEstimatedBudget] = useState("");
  const [plannedStartDate, setPlannedStartDate] = useState("");
  const [plannedEndDate, setPlannedEndDate] = useState("");
  const [mainRisks, setMainRisks] = useState("");

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [createdProject, setCreatedProject] = useState<ProjectDetail | null>(null);

  useEffect(() => {
    async function load() {
      setLoadingOrgs(true);
      const data = await getMyOrganizations();
      setOrgs(data);
      if (!organizationId && data.length > 0) {
        setOrganizationId(data[0].id);
      }
      setLoadingOrgs(false);
    }
    load();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!organizationId) {
      setError("Wybierz organizacje dla projektu");
      return;
    }

    setSaving(true);
    try {
      const project = await createProject(organizationId, {
        title,
        short_description: shortDescription,
        full_description: fullDescription || undefined,
        category,
        voivodeship: voivodeship || undefined,
        location_general: locationGeneral || undefined,
        estimated_budget: estimatedBudget || undefined,
        planned_start_date: plannedStartDate || undefined,
        planned_end_date: plannedEndDate || undefined,
        main_risks: mainRisks || undefined,
      });
      setCreatedProject(project);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Wystapil blad podczas tworzenia projektu");
    } finally {
      setSaving(false);
    }
  }

  if (createdProject) {
    return (
      <div className="max-w-2xl space-y-6">
        <div className="rounded-lg border bg-white p-6">
          <div className="flex items-center gap-2">
            <span className="inline-block h-2 w-2 rounded-full bg-green-500" />
            <h1 className="text-xl font-bold">Projekt zostal opublikowany</h1>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            Projekt jest juz widoczny publicznie w katalogu projektow.
          </p>

          <dl className="mt-4 space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-gray-500">Tytul</dt>
              <dd className="font-medium">{createdProject.title}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Status</dt>
              <dd className="font-medium">Opublikowany</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Kategoria</dt>
              <dd className="font-medium">{createdProject.category}</dd>
            </div>
          </dl>

          <div className="mt-6 flex gap-3">
            <a
              href={`/projekty/${createdProject.slug}`}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
            >
              Zobacz na stronie
            </a>
            <button
              onClick={() => {
                setCreatedProject(null);
                setTitle("");
                setShortDescription("");
                setFullDescription("");
                setVoivodeship("");
                setLocationGeneral("");
                setEstimatedBudget("");
                setPlannedStartDate("");
                setPlannedEndDate("");
                setMainRisks("");
              }}
              className="rounded-md border px-4 py-2 text-sm font-medium hover:bg-gray-50"
            >
              Dodaj kolejny projekt
            </button>
            <button
              onClick={() => router.push("/panel/projekty")}
              className="rounded-md border px-4 py-2 text-sm font-medium hover:bg-gray-50"
            >
              Wszystkie projekty
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Nowy projekt</h1>
        <p className="mt-1 text-sm text-gray-500">
          Projekt zostanie opublikowany od razu po zapisaniu
        </p>
      </div>

      <form onSubmit={handleSubmit} className="rounded-lg border bg-white p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Organizacja *</label>
          {loadingOrgs ? (
            <p className="mt-1 text-sm text-gray-500">Ladowanie organizacji...</p>
          ) : orgs.length === 0 ? (
            <p className="mt-1 text-sm text-red-600">
              Nie masz jeszcze zadnej organizacji. Utworz ja najpierw w sekcji Organizacje.
            </p>
          ) : (
            <select
              value={organizationId}
              onChange={(e) => setOrganizationId(e.target.value)}
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            >
              {orgs.map((org) => (
                <option key={org.id} value={org.id}>
                  {org.name}
                </option>
              ))}
            </select>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Tytul projektu *</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            minLength={3}
            maxLength={255}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Krotki opis * (10-500 znakow)</label>
          <textarea
            value={shortDescription}
            onChange={(e) => setShortDescription(e.target.value)}
            required
            minLength={10}
            maxLength={500}
            rows={2}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Pelny opis (opcjonalnie)</label>
          <textarea
            value={fullDescription}
            onChange={(e) => setFullDescription(e.target.value)}
            rows={5}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Kategoria *</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          >
            {CATEGORIES.map((c) => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Wojewodztwo</label>
            <input
              type="text"
              value={voivodeship}
              onChange={(e) => setVoivodeship(e.target.value)}
              maxLength={100}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Lokalizacja (miasto/gmina)</label>
            <input
              type="text"
              value={locationGeneral}
              onChange={(e) => setLocationGeneral(e.target.value)}
              maxLength={255}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Szacowany budzet (PLN)</label>
          <input
            type="number"
            step="0.01"
            min="0"
            value={estimatedBudget}
            onChange={(e) => setEstimatedBudget(e.target.value)}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Planowany start</label>
            <input
              type="date"
              value={plannedStartDate}
              onChange={(e) => setPlannedStartDate(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Planowane zakonczenie</label>
            <input
              type="date"
              value={plannedEndDate}
              onChange={(e) => setPlannedEndDate(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Glowne ryzyka (opcjonalnie)</label>
          <textarea
            value={mainRisks}
            onChange={(e) => setMainRisks(e.target.value)}
            rows={3}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={saving || orgs.length === 0}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {saving ? "Publikowanie..." : "Opublikuj projekt"}
        </button>
      </form>
    </div>
  );
}

export default function NowyProjektPage() {
  return (
    <ProtectedRoute allowedRoles={["moderator", "admin"]}>
      <NowyProjektContent />
    </ProtectedRoute>
  );
}
