import { getPublishedProjects } from "@/lib/api";
import { ProjectCard } from "@/components/ProjectCard";

export default async function ProjectsPage() {
  const projects = await getPublishedProjects();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Katalog projektow</h1>
      {projects.length === 0 ? (
        <p className="text-gray-500">
          Brak opublikowanych projektow. Wroc pozniej lub skontaktuj sie z administracja.
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}
    </div>
  );
}
