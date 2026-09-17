"use client";

import { useState, FormEvent, ChangeEvent } from "react";
import { submitComplaint, ComplaintCreatePayload } from "@/lib/api";

export default function SkargiPage() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState<ComplaintCreatePayload>({
    last_name: "",
    first_name: "",
    company_name: "",
    registration_number: "",
    street_address: "",
    postal_code: "",
    city: "",
    country: "",
    email: "",
    phone: "",
    rep_last_name: "",
    rep_first_name: "",
    rep_entity_name: "",
    rep_registration_number: "",
    rep_street_address: "",
    rep_postal_code: "",
    rep_city: "",
    rep_country: "",
    rep_email: "",
    rep_phone: "",
    project_reference: "",
    complaint_description: "",
    incident_dates: "",
    damage_description: "",
    additional_remarks: "",
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await submitComplaint(form);
      setSuccess(true);
      setForm({
        last_name: "", first_name: "", company_name: "", registration_number: "",
        street_address: "", postal_code: "", city: "", country: "", email: "",
        phone: "", rep_last_name: "", rep_first_name: "", rep_entity_name: "",
        rep_registration_number: "", rep_street_address: "", rep_postal_code: "",
        rep_city: "", rep_country: "", rep_email: "", rep_phone: "",
        project_reference: "", complaint_description: "", incident_dates: "",
        damage_description: "", additional_remarks: "",
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Nieznany błąd");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="text-2xl font-semibold mb-6">Formularz skargi</h1>

      {success && (
        <div className="mb-6 rounded border border-green-200 bg-green-50 p-4 text-green-800">
          Dziękujemy za zgłoszenie. Twoja skarga została przyjęta do rozpatrzenia.
        </div>
      )}

      {error && (
        <div className="mb-6 rounded border border-red-200 bg-red-50 p-4 text-red-800">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        <section className="space-y-4">
          <h2 className="text-lg font-medium">1. Dane skarżącego</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input label="Nazwisko *" name="last_name" value={form.last_name} onChange={handleChange} required />
            <Input label="Imię *" name="first_name" value={form.first_name} onChange={handleChange} required />
            <Input label="Nazwa firmy" name="company_name" value={form.company_name} onChange={handleChange} />
            <Input label="NIP / REGON" name="registration_number" value={form.registration_number} onChange={handleChange} />
            <Input label="Ulica i numer" name="street_address" value={form.street_address} onChange={handleChange} className="sm:col-span-2" />
            <Input label="Kod pocztowy" name="postal_code" value={form.postal_code} onChange={handleChange} />
            <Input label="Miejscowość" name="city" value={form.city} onChange={handleChange} />
            <Input label="Kraj" name="country" value={form.country} onChange={handleChange} />
            <Input label="E-mail *" name="email" type="email" value={form.email} onChange={handleChange} required />
            <Input label="Telefon" name="phone" value={form.phone} onChange={handleChange} />
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-lg font-medium">2. Dane pełnomocnika (opcjonalnie)</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input label="Nazwisko" name="rep_last_name" value={form.rep_last_name} onChange={handleChange} />
            <Input label="Imię" name="rep_first_name" value={form.rep_first_name} onChange={handleChange} />
            <Input label="Nazwa podmiotu" name="rep_entity_name" value={form.rep_entity_name} onChange={handleChange} />
            <Input label="NIP / REGON" name="rep_registration_number" value={form.rep_registration_number} onChange={handleChange} />
            <Input label="Ulica i numer" name="rep_street_address" value={form.rep_street_address} onChange={handleChange} className="sm:col-span-2" />
            <Input label="Kod pocztowy" name="rep_postal_code" value={form.rep_postal_code} onChange={handleChange} />
            <Input label="Miejscowość" name="rep_city" value={form.rep_city} onChange={handleChange} />
            <Input label="Kraj" name="rep_country" value={form.rep_country} onChange={handleChange} />
            <Input label="E-mail" name="rep_email" type="email" value={form.rep_email} onChange={handleChange} />
            <Input label="Telefon" name="rep_phone" value={form.rep_phone} onChange={handleChange} />
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-lg font-medium">3. Informacje dotyczące skargi</h2>
          <div className="grid grid-cols-1 gap-4">
            <Input label="Numer projektu / odniesienie" name="project_reference" value={form.project_reference} onChange={handleChange} />
            <Textarea label="Opis skargi *" name="complaint_description" value={form.complaint_description} onChange={handleChange} required rows={6} />
            <Input label="Daty zdarzeń" name="incident_dates" value={form.incident_dates} onChange={handleChange} placeholder="np. 2026-09-01, 2026-09-10" />
            <Textarea label="Opis szkody / straty" name="damage_description" value={form.damage_description} onChange={handleChange} rows={4} />
            <Textarea label="Dodatkowe uwagi" name="additional_remarks" value={form.additional_remarks} onChange={handleChange} rows={4} />
          </div>
        </section>

        <div className="pt-4">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center rounded bg-blue-600 px-5 py-2.5 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Wysyłanie..." : "Wyślij skargę"}
          </button>
        </div>
      </form>
    </div>
  );
}

function Input({
  label,
  name,
  value,
  onChange,
  type = "text",
  required,
  placeholder,
  className,
}: {
  label: string;
  name: string;
  value: string | undefined;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  type?: string;
  required?: boolean;
  placeholder?: string;
  className?: string;
}) {
  return (
    <label className={`block ${className || ""}`}>
      <span className="block text-sm font-medium text-gray-700 mb-1">{label}</span>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        placeholder={placeholder}
        className="w-full rounded border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      />
    </label>
  );
}

function Textarea({
  label,
  name,
  value,
  onChange,
  required,
  rows = 4,
}: {
  label: string;
  name: string;
  value: string | undefined;
  onChange: (e: ChangeEvent<HTMLTextAreaElement>) => void;
  required?: boolean;
  rows?: number;
}) {
  return (
    <label className="block">
      <span className="block text-sm font-medium text-gray-700 mb-1">{label}</span>
      <textarea
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        rows={rows}
        className="w-full rounded border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      />
    </label>
  );
}
