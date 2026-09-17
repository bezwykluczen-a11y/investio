import Link from "next/link";
import type { ProjectSummary } from "@/lib/api";

const categoryLabels: Record<string, string> = {
  housing: "Nieruchomosci mieszkaniowe",
  energy_biogas: "Energia i biogaz",
  local_infrastructure: "Infrastruktura lokalna",
  sports_recreation: "Sport i rekreacja",
  industrial: "Przemysl",
  municipal: "Projekty komunalne",
  other: "Inne",
};

export function ProjectCard({ project }: { project: ProjectSummary }) {
  return (
    <Link
      href={`/projekty/${project.slug}`}
      className="block overflow-hidden rounded-lg border bg-white hover:shadow-md transition-shadow"
    >
      {project.cover_image_url ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={project.cover_image_url}
          alt={project.title}
          className="h-40 w-full object-cover"
        />
      ) : (
        <div className="flex h-40 w-full items-center justify-center bg-gray-100 text-sm text-gray-400">
          Brak zdjecia
        </div>
      )}
      <div className="p-5">
        <span className="text-xs font-medium text-gray-500 uppercase">
          {categoryLabels[project.category] ?? project.category}
        </span>
        <h3 className="mt-1 text-lg font-semibold">{project.title}</h3>
        <p className="mt-2 text-sm text-gray-600 line-clamp-3">{project.short_description}</p>
        {project.location_general && (
          <p className="mt-3 text-xs text-gray-500">{project.location_general}</p>
        )}
      </div>
    </Link>
  );
}
