"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getAllProjects, deleteProject, ProjectSummary } from "@/lib/api";

const STATUS_LABELS: Record<string, string> = {
  draft: "Szkic",
  submitted: "Zgloszony",
  in_review: "W recenzji",
  needs_changes: "Wymaga poprawek",
  verified: "Zweryfikowany",
  published: "Opublikowany",
  paused: "Wstrzymany",
  completed: "Zakonczony",
  rejected: "Odrzucony",
};

function ProjektyContent() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [confirmingId, setConfirmingId] = useState<string | null>(null);

  async function loadProjects() {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllProjects();
      setProjects(data);
    } catch {
      setError("Nie udalo sie wczytac listy projektow");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function handleDelete(id: string) {
    setDeletingId(id);
    try {
      await deleteProject(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
      setConfirmingId(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Nie udalo sie usunac projektu");
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="max-w-4xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Wszystkie projekty</h1>
          <p className="mt-1 text-sm text-gray-500">
            Zarzadzaj projektami dodanymi na platformie
          </p>
        </div>
        <Link
          href="/panel/nowy-projekt"
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
        >
          Nowy projekt
        </Link>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {loading ? (
        <p className="text-gray-500">Ladowanie...</p>
      ) : projects.length === 0 ? (
        <p className="text-gray-600">Brak projektow.</p>
      ) : (
        <div className="space-y-3">
          {projects.map((project) => (
            <div
              key={project.id}
              className="flex items-center justify-between rounded-lg border bg-white p-4"
            >
              <div className="min-w-0 flex-1">
                <h3 className="font-semibold truncate">{project.title}</h3>
                <p className="mt-1 text-sm text-gray-600 truncate">
                  {project.short_description}
                </p>
                <div className="mt-2 flex items-center gap-2 text-xs text-gray-500">
                  <span className="rounded-full bg-gray-100 px-2 py-0.5">
                    {STATUS_LABELS[project.status] || project.status}
                  </span>
                  {project.location_general && <span>{project.location_general}</span>}
                </div>
              </div>

              <div className="ml-4 flex shrink-0 items-center gap-2">
                <Link
                  href={`/panel/projekty/${project.id}/zdjecia`}
                  className="text-sm font-medium underline"
                >
                  Zdjecia
                </Link>

                {project.status === "published" && (
                  <a
                    href={`/projekty/${project.slug}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm font-medium underline"
                  >
                    Podglad
                  </a>
                )}

                {confirmingId === project.id ? (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-red-600">Na pewno usunac?</span>
                    <button
                      onClick={() => handleDelete(project.id)}
                      disabled={deletingId === project.id}
                      className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
                    >
                      {deletingId === project.id ? "Usuwanie..." : "Tak, usun"}
                    </button>
                    <button
                      onClick={() => setConfirmingId(null)}
                      className="rounded-md border px-3 py-1.5 text-sm font-medium hover:bg-gray-50"
                    >
                      Anuluj
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setConfirmingId(project.id)}
                    className="rounded-md border border-red-300 px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50"
                  >
                    Usun
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ProjektyPage() {
  return (
    <ProtectedRoute allowedRoles={["moderator", "admin"]}>
      <ProjektyContent />
    </ProtectedRoute>
  );
}
