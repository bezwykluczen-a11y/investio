export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Zweryfikowane projekty inwestycyjne</h1>
      <p className="text-gray-600 max-w-2xl">
        Przegladaj projekty infrastrukturalne, energetyczne i nieruchomosciowe.
        Platforma nie obsluguje platnosci - prezentujemy dokumentacje i status
        weryfikacji, a kontakt z inwestorem odbywa sie poza systemem.
      </p>
      <a
        href="/projekty"
        className="inline-block rounded-md bg-gray-900 px-5 py-2.5 text-white text-sm font-medium"
      >
        Przegladaj projekty
      </a>
    </div>
  );
}
