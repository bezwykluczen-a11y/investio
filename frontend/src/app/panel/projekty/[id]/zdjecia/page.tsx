"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  getProjectImages,
  uploadProjectImage,
  deleteProjectImage,
  ProjectImage,
} from "@/lib/api";

const MAX_SIZE_MB = 15;
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];

function ZdjeciaContent() {
  const params = useParams();
  const projectId = params.id as string;

  const [images, setImages] = useState<ProjectImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function loadImages() {
    setLoading(true);
    try {
      const data = await getProjectImages(projectId);
      setImages(data);
    } catch {
      setError("Nie udalo sie wczytac zdjec");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (projectId) loadImages();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(null);

    if (!ALLOWED_TYPES.includes(file.type)) {
      setError("Dozwolone formaty: JPG, PNG, WEBP");
      return;
    }
    if (file.size / (1024 * 1024) > MAX_SIZE_MB) {
      setError(`Plik przekracza maksymalny rozmiar ${MAX_SIZE_MB} MB`);
      return;
    }

    setUploading(true);
    try {
      const uploaded = await uploadProjectImage(projectId, file);
      setImages((prev) => [...prev, uploaded]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Nie udalo sie wgrac zdjecia");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  }

  async function handleDelete(imageId: string) {
    setDeletingId(imageId);
    try {
      await deleteProjectImage(projectId, imageId);
      setImages((prev) => prev.filter((img) => img.id !== imageId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Nie udalo sie usunac zdjecia");
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <Link href="/panel/projekty" className="text-sm text-gray-500 underline">
          &larr; Wroc do listy projektow
        </Link>
        <h1 className="mt-2 text-2xl font-bold">Zdjecia projektu</h1>
        <p className="mt-1 text-sm text-gray-500">
          Dozwolone formaty: JPG, PNG, WEBP. Maksymalny rozmiar pliku: {MAX_SIZE_MB} MB.
        </p>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <div className="rounded-lg border border-dashed bg-white p-6 text-center">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden"
          id="image-upload-input"
        />
        <label
          htmlFor="image-upload-input"
          className="inline-block cursor-pointer rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
        >
          {uploading ? "Wgrywanie..." : "Dodaj zdjecie"}
        </label>
      </div>

      {loading ? (
        <p className="text-gray-500">Ladowanie...</p>
      ) : images.length === 0 ? (
        <p className="text-gray-600">Brak zdjec dla tego projektu.</p>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
          {images.map((image) => (
            <div key={image.id} className="relative overflow-hidden rounded-lg border bg-white">
              {image.url ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  src={image.url}
                  alt={image.file_name}
                  className="h-40 w-full object-cover"
                />
              ) : (
                <div className="flex h-40 w-full items-center justify-center bg-gray-100 text-sm text-gray-400">
                  Brak podgladu
                </div>
              )}
              <div className="flex items-center justify-between gap-2 p-2">
                <span className="truncate text-xs text-gray-500">{image.file_name}</span>
                <button
                  onClick={() => handleDelete(image.id)}
                  disabled={deletingId === image.id}
                  className="shrink-0 rounded-md border border-red-300 px-2 py-1 text-xs font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
                >
                  {deletingId === image.id ? "Usuwanie..." : "Usun"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ZdjeciaPage() {
  return (
    <ProtectedRoute allowedRoles={["moderator", "admin"]}>
      <ZdjeciaContent />
    </ProtectedRoute>
  );
}
