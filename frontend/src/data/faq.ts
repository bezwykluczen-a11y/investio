export type FaqItem = {
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
          "Czas weryfikacji zalezy od kompletnosci przeslanej dokumentacji. Analityk moze zwrocic projekt do uzupelnienia (status \"wymaga zmian\") przed jego publikacja.",
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
        question: "Co oznacza status \"zakonczony\"?",
        answer:
          "Status \"zakonczony\" oznacza, ze projekt zostal zrealizowany lub zamkniety informacyjnie. Nie oznacza rozliczenia srodkow, poniewaz platforma nie prowadzi obslugi platnosci.",
      },
      {
        question: "Co sie dzieje, jesli projekt nie uzyska wymaganych pozwolen?",
        answer:
          "Projekt moze otrzymac status \"wstrzymany\" lub \"odrzucony\". Historia zmian statusu jest widoczna w dzienniku audytowym platformy.",
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
        question: "Czym jest \"deklaracja zainteresowania\"?",
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
          "Nie. Publikacja projektu nie jest gwarancja jego realizacji, uzyskania pozwolen ani osiagniecia zakladanego wyniku. Szczegoly znajdziesz na stronie \"Ryzyka\".",
      },
    ],
  },
];
