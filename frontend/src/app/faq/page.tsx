import { faqCategories } from "@/data/faq";

export default function FaqPage() {
  return (
    <div className="max-w-3xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Najczesciej zadawane pytania</h1>
        <p className="mt-2 text-gray-600">
          Odpowiedzi na najczestsze pytania dotyczace korzystania z portalu.
          Platforma nie przyjmuje platnosci ani inwestycji - wiecej informacji
          znajdziesz na stronie{" "}
          <a href="/ryzyka" className="underline">
            Informacja o ryzyku
          </a>
          .
        </p>
      </div>

      {faqCategories.map((category) => (
        <section key={category.title} className="space-y-3">
          <h2 className="text-lg font-semibold border-b pb-2">
            {category.title}
          </h2>
          <div className="space-y-2">
            {category.items.map((item) => (
              <details
                key={item.question}
                className="group rounded-md border bg-white p-4"
              >
                <summary className="cursor-pointer font-medium text-gray-900 marker:content-none flex items-center justify-between">
                  <span>{item.question}</span>
                  <span className="ml-4 text-gray-400 group-open:rotate-45 transition-transform">
                    +
                  </span>
                </summary>
                <p className="mt-3 text-sm text-gray-600">{item.answer}</p>
              </details>
            ))}
          </div>
        </section>
      ))}

      <section className="rounded-md border bg-gray-50 p-4 text-sm text-gray-600">
        Nie znalazles odpowiedzi na swoje pytanie? Skontaktuj sie z nami
        poprzez formularz kontaktowy.
      </section>
    </div>
  );
}
