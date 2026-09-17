export default function HowItWorksPage() {
  const steps = [
    "Pomyslodawca zglasza projekt i przekazuje dokumentacje formalna, techniczna i finansowa.",
    "Analityk platformy weryfikuje kompletnosc dokumentow i podstawowe ryzyka.",
    "Projekt otrzymuje status weryfikacji i, po akceptacji, zostaje opublikowany w katalogu.",
    "Zainteresowani moga zadawac pytania i zapisac sie na powiadomienia o projekcie.",
    "Platforma nie przyjmuje wplat - kontakt handlowy i finansowy odbywa sie poza systemem.",
  ];

  return (
    <div className="max-w-2xl space-y-4">
      <h1 className="text-2xl font-bold">Jak to dziala</h1>
      <ol className="list-decimal list-inside space-y-2 text-gray-700">
        {steps.map((step) => (
          <li key={step}>{step}</li>
        ))}
      </ol>
    </div>
  );
}
