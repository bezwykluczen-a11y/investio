#!/usr/bin/env python3
"""
Dodaje strone FAQ (najczesciej zadawane pytania) do projektu
mvp-portal-projektow, wraz z linkiem w nawigacji.

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 add_faq_page.py

Po uruchomieniu:
    docker compose up -d --build web
    otworz http://localhost:3001/faq
"""
import os

FILES: dict[str, str] = {}

FILES["frontend/src/data/faq.ts"] = '''export type FaqItem = {
  question: string;
  answer: string;
};

export type FaqCategory = {
  title: string;
  items: FaqItem[];
};

// Struktura pytan zainspirowana FAQ zrzutka.pl, zaadaptowana do
// platformy bez platnosci (katalog i weryfikacja projektow).
// TODO: zastapic tresci odpowiedzi wlasciwymi dla specyfiki projektu
// (osiedla, biogazownie, strzelnice) przed publikacja produkcyjna.
export const faqCategories: FaqCategory[] = [
  {
    title: "Ogolne",
    items: [
      {
        question: "Czym jest ten portal?",
        answer:
          "Portal to katalog zweryfikowanych projektow inwestycyjnych (np. osiedla mieszkaniowe, biogazownie, strzelnice). Prezentujemy dokumentacje projektu i status jego weryfikacji formalnej.",
      },
      {
        question: "Czy portal przyjmuje wplaty lub inwestycje?",
        answer:
          "Nie. Portal nie obsluguje platnosci, wplat, wyplat ani inwestycji. Zgloszenie zainteresowania projektem nie jest zobowiazaniem finansowym, oferta ani umowa.",
      },
      {
        question: "Jak zrzutka.pl zapewnia bezpieczenstwo danych - a jak dziala to u nas?",
        answer:
          "Nie przechowujemy danych platniczych. Dokumenty projektow sa dostepne przez zabezpieczone, tymczasowe odnosniki, a dostep do danych niepublicznych mają wylacznie zweryfikowani analitycy platformy.",
      },
    ],
  },
  {
    title: "Zakladanie projektu",
    items: [
      {
        question: "Jak dodac projekt do katalogu?",
        answer:
          "Po zalozeniu konta i organizacji, w panelu pomyslodawcy wypelniasz formularz projektu (opis, kategoria, lokalizacja, budzet orientacyjny, harmonogram) i przekazujesz dokumenty formalne.",
      },
      {
        question: "Jak stworzyc dobry opis projektu? Jakie informacje powinien zawierac?",
        answer:
          "Opis powinien zawierac cel projektu, lokalizacje, etap realizacji, status pozwolen, orientacyjny budzet oraz glowne ryzyka. Unikaj obietnic gwarantowanego zysku.",
      },
      {
        question: "Jakie zdjecie wybrac jako okladke projektu?",
        answer:
          "Najlepiej dzialaja zdjecia realnej lokalizacji, wizualizacje architektoniczne lub zdjecia z placu budowy. Unikaj grafik reklamowych sugerujacych gotowy efekt bez podstawy w dokumentacji.",
      },
    ],
  },
  {
    title: "Weryfikacja",
    items: [
      {
        question: "W jaki sposob dokonac weryfikacji profilu organizatora?",
        answer:
          "Weryfikacja obejmuje potwierdzenie danych organizacji (nazwa, NIP/KRS) oraz danych osob reprezentujacych. Analityk platformy sprawdza kompletnosc i wiarygodnosc przeslanych dokumentow.",
      },
      {
        question: "Jakie dokumenty trzeba przeslac w czasie weryfikacji projektu?",
        answer:
          "W zaleznosci od typu projektu: dokument potwierdzajacy prawo do gruntu, decyzje administracyjne, pozwolenia, kosztorys, harmonogram oraz - dla wybranych kategorii - opinie techniczne.",
      },
      {
        question: "Jak dlugo trwa weryfikacja projektu?",
        answer:
          "Czas weryfikacji zalezy od kompletnosci przeslanej dokumentacji. Analityk moze zwrocic projekt do uzupelnienia (status \\"wymaga zmian\\") przed jego publikacja.",
      },
    ],
  },
  {
    title: "Zarzadzanie projektem",
    items: [
      {
        question: "Czy moge edytowac projekt po jego publikacji?",
        answer:
          "Po publikacji edycja kluczowych danych jest ograniczona. Zmiany istotne dla inwestorow wymagaja ponownej weryfikacji i publikowane sa jako aktualizacja projektu.",
      },
      {
        question: "Jak dodac aktualizacje postepu projektu?",
        answer:
          "W panelu pomyslodawcy, w zakladce projektu, mozesz dodac wpis aktualizacji z opisem postepu - widoczny dla osob obserwujacych projekt.",
      },
      {
        question: "Kto moze zadawac pytania dotyczace projektu?",
        answer:
          "Kazdy zalogowany uzytkownik moze zadac pytanie pod opublikowanym projektem. Odpowiedzi udziela pomyslodawca lub administrator platformy.",
      },
    ],
  },
  {
    title: "Zakonczenie projektu",
    items: [
      {
        question: "Co oznacza status \\"zakonczony\\"?",
        answer:
          "Status \\"zakonczony\\" oznacza, ze projekt zostal zrealizowany lub zamkniety informacyjnie. Nie oznacza rozliczenia srodkow, poniewaz platforma nie prowadzi obslugi platnosci.",
      },
      {
        question: "Co sie dzieje, jesli projekt nie uzyska wymaganych pozwolen?",
        answer:
          "Projekt moze otrzymac status \\"wstrzymany\\" lub \\"odrzucony\\". Historia zmian statusu jest widoczna w dzienniku audytowym platformy.",
      },
    ],
  },
  {
    title: "Dla pomyslodawcow",
    items: [
      {
        question: "Czy muszę zaplacic za publikacje projektu?",
        answer:
          "Zasady oplat za publikacje i usluigi dodatkowe (np. wyroznienie projektu) zostana okreslone odrebnie przed wdrozeniem produkcyjnym platformy.",
      },
      {
        question: "Czy moge promowac swoj projekt poza platforma?",
        answer:
          "Tak. Mozesz udostepniac link do karty projektu w mediach spolecznosciowych i materialach wlasnych, z zachowaniem wymogow dotyczacych rzetelnosci informacji.",
      },
    ],
  },
  {
    title: "Dla zainteresowanych / obserwujacych",
    items: [
      {
        question: "Czym jest \\"deklaracja zainteresowania\\"?",
        answer:
          "To nieformalny formularz pozwalajacy zglosic chec otrzymania wiecej informacji o projekcie. Nie jest to wplata, inwestycja ani zobowiazanie finansowe.",
      },
      {
        question: "Jak obserwowac postepy projektu?",
        answer:
          "Po zalogowaniu mozesz dodac projekt do listy obserwowanych - otrzymasz wtedy widocznosc jego aktualizacji w swoim panelu.",
      },
    ],
  },
  {
    title: "Bezpieczenstwo",
    items: [
      {
        question: "Jak zglosic projekt, ktory wzbudza wątpliwosci?",
        answer:
          "Skontaktuj sie z administracja platformy przez formularz kontaktowy, podajac link do projektu i opis wątpliwosci. Zgloszenie zostanie zweryfikowane przez zespol moderacji.",
      },
      {
        question: "Czy platforma gwarantuje realizacje projektu lub zwrot zaangazowanych srodkow?",
        answer:
          "Nie. Publikacja projektu nie jest gwarancja jego realizacji, uzyskania pozwolen ani osiagniecia zakladanego wyniku. Szczegoly znajdziesz na stronie \\"Ryzyka\\".",
      },
    ],
  },
];
'''

FILES["frontend/src/app/faq/page.tsx"] = '''import { faqCategories } from "@/data/faq";

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
'''

FILES["frontend/src/app/layout.tsx"] = '''import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Portal Projektow",
  description: "Katalog i weryfikacja projektow inwestycyjnych",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pl">
      <body className="bg-gray-50 text-gray-900">
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-4 py-4 flex items-center justify-between">
            <a href="/" className="font-semibold text-lg">Portal Projektow</a>
            <nav className="flex gap-4 text-sm">
              <a href="/projekty">Projekty</a>
              <a href="/blog">Blog</a>
              <a href="/faq">FAQ</a>
              <a href="/jak-to-dziala">Jak to dziala</a>
              <a href="/ryzyka">Ryzyka</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="border-t mt-16 py-6 text-center text-sm text-gray-500">
          Ta platforma nie przyjmuje platnosci, wplat ani inwestycji. Deklaracje zainteresowania
          nie sa zobowiazaniem finansowym.
        </footer>
      </body>
    </html>
  );
}
'''


def main() -> None:
    if not os.path.exists("docker-compose.yml"):
        print("UWAGA: nie widze docker-compose.yml w tym katalogu.")
        print("Upewnij sie, ze uruchamiasz skrypt wewnatrz folderu mvp-portal-projektow.")
        return

    created = 0
    for rel_path, content in FILES.items():
        os.makedirs(os.path.dirname(rel_path) or ".", exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"  napisano: {rel_path}")

    print(f"\\nZaktualizowano/dodano {created} plikow.")
    print("\\nNastepne kroki:")
    print("  docker compose up -d --build web")
    print("  otworz http://localhost:3001/faq")


if __name__ == "__main__":
    main()
