import { getProjectBySlug, getProjectImages } from "@/lib/api";
import { notFound } from "next/navigation";
import { ProjectGallery } from "@/components/ProjectGallery";

export default async function ProjectDetailPage({ params }: { params: { slug: string } }) {
  const project = await getProjectBySlug(params.slug);
  if (!project) notFound();

  const images = await getProjectImages(project.id);

  return (
    <article className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">{project.title}</h1>
        {project.location_general && (
          <p className="text-sm text-gray-500 mt-1">{project.location_general}</p>
        )}
      </div>

      <ProjectGallery images={images} altText={project.title} />

      <p className="text-gray-700">{project.short_description}</p>

      {project.full_description && (
        <section>
          <h2 className="text-lg font-semibold mb-2">Opis projektu</h2>
          <p className="text-gray-700 whitespace-pre-line">{project.full_description}</p>
        </section>
      )}

      {project.main_risks && (
        <section className="rounded-md border border-amber-200 bg-amber-50 p-4">
          <h2 className="text-sm font-semibold text-amber-800 mb-1">Glowne ryzyka</h2>
          <p className="text-sm text-amber-800 whitespace-pre-line">{project.main_risks}</p>
        </section>
      )}

      <section className="rounded-md border bg-gray-50 p-4 text-sm text-gray-600">
        Ten portal nie przyjmuje platnosci ani inwestycji. Zgloszenie zainteresowania
        nie jest zobowiazaniem finansowym, a kontakt handlowy odbywa sie poza systemem.
      </section>
    </article>
  );
}
