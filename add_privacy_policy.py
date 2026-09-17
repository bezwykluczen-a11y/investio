#!/usr/bin/env python3
"""
Dodaje strone Polityki Prywatnosci do projektu mvp-portal-projektow,
wzorowana na strukturze zrzutka.pl, ale zaadaptowana do platformy
Investio (katalog i weryfikacja projektow inwestycyjnych, bez platnosci).

Link do polityki pojawia sie w FOOTERZE (nie w headerze).

Uzycie: uruchom WEWNATRZ folderu mvp-portal-projektow:

    cd mvp-portal-projektow
    python3 add_privacy_policy.py

Po uruchomieniu:
    docker compose up -d --build web
    otworz http://localhost:3001/polityka-prywatnosci
"""
import os

FILES: dict[str, str] = {}

FILES["frontend/src/app/polityka-prywatnosci/page.tsx"] = '''export const metadata = {
  title: "Polityka prywatnosci - Investio",
};

export default function PrivacyPolicyPage() {
  return (
    <div className="max-w-3xl space-y-8 text-gray-700">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Polityka prywatnosci</h1>
        <p className="mt-2 text-sm text-gray-500">
          Ostatnia aktualizacja: 13 sierpnia 2026 r.
        </p>
      </div>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">1. Wstep</h2>
        <p>
          Niniejsza Polityka Prywatnosci okresla zasady gromadzenia, przetwarzania
          i ochrony danych osobowych Uzytkownikow korzystajacych z serwisu
          internetowego Investio, dostepnego pod adresem [adres domeny - do
          uzupelnienia].
        </p>
        <p>
          Dokument ten ma charakter informacyjny i wzorowany jest na dobrych
          praktykach rynkowych. Przed wdrozeniem produkcyjnym platformy polityka
          powinna zostac zweryfikowana przez prawnika pod katem faktycznego modelu
          dzialalnosci, struktury spolki oraz wymogow regulacyjnych.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">2. Definicje</h2>
        <ul className="list-disc list-inside space-y-1">
          <li>
            <strong>Administrator</strong> - [nazwa spolki, adres siedziby, NIP,
            KRS, REGON - do uzupelnienia przed publikacja produkcyjna], bedaca
            administratorem danych osobowych Uzytkownikow.
          </li>
          <li>
            <strong>Serwis</strong> - serwis internetowy Investio, w ramach
            ktorego Administrator udostepnia katalog i system weryfikacji
            projektow inwestycyjnych.
          </li>
          <li>
            <strong>Uzytkownik</strong> - osoba fizyczna, osoba prawna lub
            jednostka organizacyjna korzystajaca z Serwisu.
          </li>
          <li>
            <strong>Pomyslodawca</strong> - Uzytkownik, ktory zglasza projekt do
            weryfikacji i publikacji w katalogu Serwisu.
          </li>
          <li>
            <strong>RODO</strong> - Rozporzadzenie Parlamentu Europejskiego i
            Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r. w sprawie ochrony
            osob fizycznych w zwiazku z przetwarzaniem danych osobowych.
          </li>
        </ul>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          3. Jakie dane osobowe gromadzimy
        </h2>
        <p>
          W zaleznosci od sposobu korzystania z Serwisu, mozemy przetwarzac
          nastepujace kategorie danych:
        </p>
        <ul className="list-disc list-inside space-y-1">
          <li>
            <strong>Rejestracja konta:</strong> imie, nazwisko, adres e-mail,
            haslo (przechowywane w postaci zaszyfrowanej).
          </li>
          <li>
            <strong>Profil organizacji (Pomyslodawca):</strong> nazwa organizacji,
            dane rejestrowe (NIP, KRS), dane osob reprezentujacych organizacje.
          </li>
          <li>
            <strong>Dane kontaktowe:</strong> adres e-mail i inne dane podane
            dobrowolnie w formularzach kontaktowych lub deklaracjach
            zainteresowania projektem.
          </li>
          <li>
            <strong>Dane techniczne:</strong> adres IP, typ przegladarki, dane o
            aktywnosci w Serwisie - wykorzystywane do celow analitycznych,
            statystycznych i bezpieczenstwa.
          </li>
        </ul>
        <p>
          Serwis nie przyjmuje platnosci ani wplat, dlatego nie przetwarzamy
          danych kart platniczych ani danych transakcji finansowych.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          4. Cele i podstawy prawne przetwarzania
        </h2>
        <ul className="list-disc list-inside space-y-1">
          <li>
            <strong>Zalozenie i obsluga konta</strong> - podstawa: art. 6 ust. 1
            lit. b RODO (wykonanie umowy).
          </li>
          <li>
            <strong>Weryfikacja projektow i organizacji</strong> - podstawa: art.
            6 ust. 1 lit. b RODO (wykonanie umowy) oraz art. 6 ust. 1 lit. f
            RODO (prawnie uzasadniony interes Administratora).
          </li>
          <li>
            <strong>Odpowiedzi na zapytania i formularz kontaktowy</strong> -
            podstawa: art. 6 ust. 1 lit. b RODO.
          </li>
          <li>
            <strong>Cele analityczne, statystyczne i marketingowe</strong> -
            podstawa: art. 6 ust. 1 lit. f RODO (uzasadniony interes) lub art. 6
            ust. 1 lit. a RODO (zgoda, jesli zostala udzielona).
          </li>
          <li>
            <strong>Obowiazki prawne i podatkowe</strong> - podstawa: art. 6
            ust. 1 lit. c RODO.
          </li>
        </ul>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          5. Komu udostepniamy dane
        </h2>
        <p>
          Dane osobowe moga byc udostepniane podmiotom trzecim wylacznie w
          zakresie niezbednym do realizacji uslug, w szczegolnosci:
        </p>
        <ul className="list-disc list-inside space-y-1">
          <li>dostawcom uslug IT i hostingowych (serwery, infrastruktura),</li>
          <li>dostawcom uslug analitycznych (np. Google Analytics),</li>
          <li>podmiotom swiadczacym uslugi prawne, ksiegowe i audytowe,</li>
          <li>organom publicznym - gdy wymagaja tego przepisy prawa.</li>
        </ul>
        <p>
          Z kazdym podmiotem, ktoremu powierzamy przetwarzanie danych, zawieramy
          umowe powierzenia przetwarzania danych osobowych, zgodnie z wymogami
          RODO.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          6. Okres przechowywania danych
        </h2>
        <p>
          Dane osobowe przechowujemy przez okres niezbedny do realizacji celow,
          dla ktorych zostaly zebrane, a nastepnie przez okres wymagany
          przepisami prawa (np. przepisy podatkowe, ksiegowe). Dane konta
          przechowujemy do momentu jego usuniecia przez Uzytkownika, z
          zastrzezeniem obowiazkow ustawowych.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          7. Prawa Uzytkownika
        </h2>
        <p>Zgodnie z RODO, przysluguje Ci prawo do:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>dostepu do swoich danych osobowych,</li>
          <li>sprostowania (poprawiania) danych,</li>
          <li>usuniecia danych (prawo do bycia zapomnianym),</li>
          <li>ograniczenia przetwarzania,</li>
          <li>przenoszenia danych,</li>
          <li>wniesienia sprzeciwu wobec przetwarzania,</li>
          <li>cofniecia zgody w dowolnym momencie (jesli przetwarzanie odbywa
            sie na podstawie zgody),</li>
          <li>wniesienia skargi do organu nadzorczego - Prezesa Urzedu Ochrony
            Danych Osobowych (UODO).</li>
        </ul>
        <p>
          Wniosek dotyczacy realizacji praw mozesz zlozyc pisemnie na adres
          Administratora lub elektronicznie na adres e-mail: [adres e-mail - do
          uzupelnienia].
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          8. Pliki cookies i narzedzia analityczne
        </h2>
        <p>
          Serwis wykorzystuje pliki cookies w celu zapewnienia prawidlowego
          dzialania, analizy ruchu i poprawy funkcjonalnosci. Szczegolowe
          informacje na temat stosowanych narzedzi analitycznych (np. Google
          Analytics) oraz sposobu zarzadzania plikami cookies znajdziesz w
          ustawieniach swojej przegladarki internetowej.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          9. Bezpieczenstwo danych
        </h2>
        <p>
          Stosujemy srodki techniczne i organizacyjne majace na celu ochrone
          danych osobowych, w tym szyfrowanie polaczen (SSL/TLS), kontrole
          dostepu, uwierzytelnianie wieloskladnikowe dla personelu oraz
          regularne kopie zapasowe. Dostep do danych osobowych maja wylacznie
          osoby upowaznione, zobowiazane do zachowania poufnosci.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">
          10. Zmiany w Polityce Prywatnosci
        </h2>
        <p>
          Administrator zastrzega sobie prawo do wprowadzania zmian w niniejszej
          Polityce Prywatnosci. O istotnych zmianach Uzytkownicy zostana
          poinformowani za posrednictwem Serwisu lub droga elektroniczna.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-900">11. Kontakt</h2>
        <p>
          W sprawach zwiazanych z ochrona danych osobowych mozesz skontaktowac
          sie z Administratorem pod adresem: [adres korespondencyjny - do
          uzupelnienia] lub e-mail: [adres e-mail - do uzupelnienia].
        </p>
      </section>

      <section className="rounded-md border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
        <strong>Uwaga:</strong> Niniejsza Polityka Prywatnosci ma charakter
        wzorowy i zostala przygotowana na potrzeby wersji MVP platformy. Przed
        wdrozeniem produkcyjnym nalezy uzupelnic dane Administratora (nazwa
        spolki, adres, NIP, KRS, REGON, adres e-mail) oraz skonsultowac tresc z
        prawnikiem pod katem faktycznego modelu dzialalnosci, regulacji
        sektorowych oraz wymogow RODO.
      </section>
    </div>
  );
}
'''

FILES["frontend/src/app/layout.tsx"] = '''import "./globals.css";
import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";

export const metadata = {
  title: "Investio",
  description: "Katalog i weryfikacja projektow inwestycyjnych",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pl">
      <body className="bg-gray-50 text-gray-900">
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-4 py-2 flex items-center justify-between">
            <Link href="/" className="flex items-center shrink-0">
              <Image
                src="/logo.png"
                alt="Investio"
                width={400}
                height={100}
                priority
                className="h-16 w-auto object-contain"
              />
            </Link>
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
          <div className="space-y-2">
            <p>
              Ta platforma nie przyjmuje platnosci, wplat ani inwestycji.
              Deklaracje zainteresowania nie sa zobowiazaniem finansowym.
            </p>
            <p>
              <a href="/polityka-prywatnosci" className="underline hover:text-gray-700">
                Polityka prywatnosci
              </a>
            </p>
          </div>
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
    print("  otworz http://localhost:3001/polityka-prywatnosci")
    print("\\nWAZNE: przed publikacja produkcyjna uzupelnij w tresci:")
    print("  - nazwe spolki, adres siedziby, NIP, KRS, REGON")
    print("  - adres e-mail kontaktowy")
    print("  - adres domeny platformy")
    print("  - skonsultuj tresc z prawnikiem")


if __name__ == "__main__":
    main()
