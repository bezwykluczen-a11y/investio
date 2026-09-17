"use client";

import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

type UserProfile = {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  notify_email_project_updates: boolean;
  notify_email_new_projects: boolean;
  notify_email_marketing: boolean;
};

type FeedbackState = { type: "success" | "error"; message: string } | null;

function ProfileSection({
  profile,
  onUpdated,
}: {
  profile: UserProfile;
  onUpdated: (p: UserProfile) => void;
}) {
  const [fullName, setFullName] = useState(profile.full_name);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState<FeedbackState>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setFeedback(null);
    try {
      const res = await fetch(`${API_URL}/me/profile`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify({ full_name: fullName }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Nie udalo sie zapisac profilu");
      }
      const updated = await res.json();
      onUpdated(updated);
      setFeedback({ type: "success", message: "Profil zostal zaktualizowany" });
    } catch (err) {
      setFeedback({
        type: "error",
        message: err instanceof Error ? err.message : "Wystapil blad",
      });
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="rounded-lg border bg-white p-6">
      <h2 className="text-lg font-semibold">Profil</h2>
      <p className="mt-1 text-sm text-gray-600">Podstawowe informacje o Twoim koncie</p>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4 max-w-md">
        <div>
          <label className="block text-sm font-medium text-gray-700">Adres e-mail</label>
          <input
            type="email"
            value={profile.email}
            disabled
            className="mt-1 block w-full rounded-md border border-gray-300 bg-gray-50 px-3 py-2 text-sm text-gray-500"
          />
          <p className="mt-1 text-xs text-gray-400">Adres e-mail nie moze byc zmieniony</p>
        </div>

        <div>
          <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
            Imie i nazwisko
          </label>
          <input
            id="full_name"
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            minLength={2}
            maxLength={255}
            required
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        {feedback && (
          <p className={feedback.type === "success" ? "text-sm text-green-600" : "text-sm text-red-600"}>
            {feedback.message}
          </p>
        )}

        <button
          type="submit"
          disabled={saving}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {saving ? "Zapisywanie..." : "Zapisz zmiany"}
        </button>
      </form>
    </section>
  );
}

function PasswordSection() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState<FeedbackState>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFeedback(null);

    if (newPassword !== confirmPassword) {
      setFeedback({ type: "error", message: "Nowe hasla nie sa identyczne" });
      return;
    }
    if (newPassword.length < 8) {
      setFeedback({ type: "error", message: "Nowe haslo musi miec co najmniej 8 znakow" });
      return;
    }

    setSaving(true);
    try {
      const res = await fetch(`${API_URL}/me/password`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Nie udalo sie zmienic hasla");
      }
      setFeedback({ type: "success", message: "Haslo zostalo zmienione" });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setFeedback({
        type: "error",
        message: err instanceof Error ? err.message : "Wystapil blad",
      });
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="rounded-lg border bg-white p-6">
      <h2 className="text-lg font-semibold">Zmiana hasla</h2>
      <p className="mt-1 text-sm text-gray-600">Uzyj silnego, unikalnego hasla</p>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4 max-w-md">
        <div>
          <label htmlFor="current_password" className="block text-sm font-medium text-gray-700">
            Obecne haslo
          </label>
          <input
            id="current_password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        <div>
          <label htmlFor="new_password" className="block text-sm font-medium text-gray-700">
            Nowe haslo
          </label>
          <input
            id="new_password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            minLength={8}
            maxLength={128}
            required
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        <div>
          <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">
            Potwierdz nowe haslo
          </label>
          <input
            id="confirm_password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            minLength={8}
            maxLength={128}
            required
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none"
          />
        </div>

        {feedback && (
          <p className={feedback.type === "success" ? "text-sm text-green-600" : "text-sm text-red-600"}>
            {feedback.message}
          </p>
        )}

        <button
          type="submit"
          disabled={saving}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {saving ? "Zapisywanie..." : "Zmien haslo"}
        </button>
      </form>
    </section>
  );
}

function NotificationsSection({
  profile,
  onUpdated,
}: {
  profile: UserProfile;
  onUpdated: (p: UserProfile) => void;
}) {
  const [projectUpdates, setProjectUpdates] = useState(profile.notify_email_project_updates);
  const [newProjects, setNewProjects] = useState(profile.notify_email_new_projects);
  const [marketing, setMarketing] = useState(profile.notify_email_marketing);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState<FeedbackState>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setFeedback(null);
    try {
      const res = await fetch(`${API_URL}/me/notifications`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify({
          notify_email_project_updates: projectUpdates,
          notify_email_new_projects: newProjects,
          notify_email_marketing: marketing,
        }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Nie udalo sie zapisac preferencji");
      }
      const updated = await res.json();
      onUpdated(updated);
      setFeedback({ type: "success", message: "Preferencje zostaly zapisane" });
    } catch (err) {
      setFeedback({
        type: "error",
        message: err instanceof Error ? err.message : "Wystapil blad",
      });
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="rounded-lg border bg-white p-6">
      <h2 className="text-lg font-semibold">Powiadomienia</h2>
      <p className="mt-1 text-sm text-gray-600">Wybierz, jakie e-maile chcesz otrzymywac</p>

      <form onSubmit={handleSubmit} className="mt-4 space-y-4 max-w-md">
        <label className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={projectUpdates}
            onChange={(e) => setProjectUpdates(e.target.checked)}
            className="mt-1 h-4 w-4 rounded border-gray-300"
          />
          <span>
            <span className="block text-sm font-medium text-gray-900">
              Aktualizacje obserwowanych projektow
            </span>
            <span className="block text-xs text-gray-500">
              Zmiany statusu i nowe informacje o projektach, ktore obserwujesz
            </span>
          </span>
        </label>

        <label className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={newProjects}
            onChange={(e) => setNewProjects(e.target.checked)}
            className="mt-1 h-4 w-4 rounded border-gray-300"
          />
          <span>
            <span className="block text-sm font-medium text-gray-900">Nowe projekty</span>
            <span className="block text-xs text-gray-500">
              Powiadomienie o publikacji nowych projektow inwestycyjnych
            </span>
          </span>
        </label>

        <label className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={marketing}
            onChange={(e) => setMarketing(e.target.checked)}
            className="mt-1 h-4 w-4 rounded border-gray-300"
          />
          <span>
            <span className="block text-sm font-medium text-gray-900">Materialy marketingowe</span>
            <span className="block text-xs text-gray-500">
              Newsletter, oferty i informacje promocyjne
            </span>
          </span>
        </label>

        {feedback && (
          <p className={feedback.type === "success" ? "text-sm text-green-600" : "text-sm text-red-600"}>
            {feedback.message}
          </p>
        )}

        <button
          type="submit"
          disabled={saving}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-50"
        >
          {saving ? "Zapisywanie..." : "Zapisz preferencje"}
        </button>
      </form>
    </section>
  );
}

function UstawieniaContent() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProfile() {
      const token = getToken();
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API_URL}/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Nie udalo sie wczytac profilu");
        const data = await res.json();
        setProfile(data);
      } catch {
        setLoadError("Nie udalo sie wczytac danych konta. Sprobuj odswiezyc strone.");
      } finally {
        setLoading(false);
      }
    }
    fetchProfile();
  }, []);

  if (loading) return <p className="text-gray-500">Ladowanie...</p>;
  if (loadError) return <p className="text-red-600">{loadError}</p>;
  if (!profile) return <p className="text-gray-500">Brak danych konta.</p>;

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Ustawienia</h1>
        <p className="mt-1 text-sm text-gray-500">
          Zarzadzaj profilem, haslem i powiadomieniami
        </p>
      </div>

      <ProfileSection profile={profile} onUpdated={setProfile} />
      <PasswordSection />
      <NotificationsSection profile={profile} onUpdated={setProfile} />
    </div>
  );
}

export default function UstawieniaPage() {
  return (
    <ProtectedRoute>
      <UstawieniaContent />
    </ProtectedRoute>
  );
}
