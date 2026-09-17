import { getAuthHeaders } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type ProjectSummary = {
  id: string;
  organization_id: string;
  title: string;
  slug: string;
  short_description: string;
  category: string;
  status: string;
  voivodeship: string | null;
  location_general: string | null;
  estimated_budget: string | null;
  cover_image_url: string | null;
};

export type ProjectDetail = ProjectSummary & {
  full_description: string | null;
  main_risks: string | null;
  planned_start_date: string | null;
  planned_end_date: string | null;
};

export async function getPublishedProjects(params?: {
  category?: string;
  voivodeship?: string;
}): Promise<ProjectSummary[]> {
  const search = new URLSearchParams();
  if (params?.category) search.set("category", params.category);
  if (params?.voivodeship) search.set("voivodeship", params.voivodeship);
  const res = await fetch(`${API_URL}/projects?${search.toString()}`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function getProjectBySlug(slug: string): Promise<ProjectDetail | null> {
  const res = await fetch(`${API_URL}/projects/${slug}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export async function getAllProjects(statusFilter?: string): Promise<ProjectSummary[]> {
  const search = new URLSearchParams();
  if (statusFilter) search.set("status_filter", statusFilter);
  const res = await fetch(`${API_URL}/admin/projects?${search.toString()}`, {
    headers: getAuthHeaders(),
    cache: "no-store",
  });
  if (!res.ok) return [];
  return res.json();
}

export async function deleteProject(projectId: string): Promise<void> {
  const res = await fetch(`${API_URL}/projects/${projectId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udalo sie usunac projektu");
  }
}

export type Organization = {
  id: string;
  name: string;
  slug: string;
  legal_name: string | null;
  is_verified: boolean;
};

export type OrganizationCreatePayload = {
  name: string;
  legal_name?: string;
  nip?: string;
  krs?: string;
  description?: string;
};

export async function getMyOrganizations(): Promise<Organization[]> {
  const res = await fetch(`${API_URL}/organizations/me/list`, {
    headers: getAuthHeaders(),
    cache: "no-store",
  });
  if (!res.ok) return [];
  return res.json();
}

export async function createOrganization(payload: OrganizationCreatePayload): Promise<Organization> {
  const res = await fetch(`${API_URL}/organizations`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeaders() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udalo sie utworzyc organizacji");
  }
  return res.json();
}

export type ProjectCreatePayload = {
  title: string;
  short_description: string;
  full_description?: string;
  category: string;
  voivodeship?: string;
  location_general?: string;
  estimated_budget?: string;
  planned_start_date?: string;
  planned_end_date?: string;
  main_risks?: string;
};

export async function createProject(
  organizationId: string,
  payload: ProjectCreatePayload
): Promise<ProjectDetail> {
  const res = await fetch(`${API_URL}/projects/organizations/${organizationId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeaders() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udalo sie utworzyc projektu");
  }
  return res.json();
}

export async function submitProject(projectId: string): Promise<ProjectDetail> {
  const res = await fetch(`${API_URL}/projects/${projectId}/submit`, {
    method: "POST",
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udalo sie zglosic projektu do recenzji");
  }
  return res.json();
}

export type ProjectImage = {
  id: string;
  project_id: string;
  file_name: string;
  content_type: string;
  size_bytes: number;
  is_public: boolean;
  status: string;
  url: string | null;
};

export async function getProjectImages(projectId: string): Promise<ProjectImage[]> {
  const res = await fetch(`${API_URL}/projects/${projectId}/images`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function uploadProjectImage(projectId: string, file: File): Promise<ProjectImage> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_URL}/projects/${projectId}/images`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udalo sie wgrac zdjecia");
  }
  return res.json();
}

export async function deleteProjectImage(projectId: string, imageId: string): Promise<void> {
  const res = await fetch(`${API_URL}/projects/${projectId}/images/${imageId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udalo sie usunac zdjecia");
  }
}


export type ComplaintCreatePayload = {
  last_name: string;
  first_name: string;
  company_name?: string;
  registration_number?: string;
  street_address?: string;
  postal_code?: string;
  city?: string;
  country?: string;
  email: string;
  phone?: string;
  rep_last_name?: string;
  rep_first_name?: string;
  rep_entity_name?: string;
  rep_registration_number?: string;
  rep_street_address?: string;
  rep_postal_code?: string;
  rep_city?: string;
  rep_country?: string;
  rep_email?: string;
  rep_phone?: string;
  project_reference?: string;
  complaint_description: string;
  incident_dates?: string;
  damage_description?: string;
  additional_remarks?: string;
};

export async function submitComplaint(payload: ComplaintCreatePayload): Promise<{ id: string; status: string; created_at: string }> {
  const res = await fetch(`${API_URL}/complaints`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Nie udało się wysłać skargi");
  }
  return res.json();
}
