import Image from "next/image";

export const metadata = {
  title: "O nas - Investio",
  description: "Investio - łączymy kapitał z dobrymi projektami",
};

export default function ONasPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-12">
      <section className="space-y-6">
        <h1 className="text-3xl font-bold">O nas</h1>
        <p className="text-lg text-gray-700">
          <strong>Investio</strong> to platforma łącząca kapitał z dobrymi projektami inwestycyjnymi.
          Nasza misja jest prosta: chcemy ułatwiać dostęp do finansowania tym, którzy tworzą wartościowe przedsięwzięcia,
          jednocześnie dając inwestorom możliwość uczestnictwa w przemyślanych, transparentnych projektach.
        </p>
      </section>

      <section className="grid gap-8 sm:grid-cols-2">
        <div className="space-y-3">
          <h2 className="text-xl font-semibold">Łączymy kapitał z projektami</h2>
          <p className="text-gray-700">
            Investio łączy osoby i podmioty dysponujące kapitałem z organizatorami projektów,
            którzy poszukują finansowania na ich rozwój. Dzięki temu inwestorzy mają dostęp do starannie wyselekcjonowanych okazji,
            a organizatorzy zyskują wsparcie niezbędne do realizacji swoich planów.
          </p>
        </div>
        <div className="space-y-3">
          <h2 className="text-xl font-semibold">Budujemy relacje</h2>
          <p className="text-gray-700">
            Nasza wizja opiera się na budowaniu długoterminowych, opartych na zaufaniu relacji
            pomiędzy wszystkimi uczestnikami procesu. Dążymy do tego, aby każdy inwestor mógł czerpać korzyści
            z dobrze przygotowanych projektów, a organizatorzy mogli realizować swoje założenia w terminie.
          </p>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Jak to działa?</h2>
        <ol className="list-decimal list-inside space-y-2 text-gray-700">
          <li><strong>Zgłoszenie projektu</strong> – organizator przesyła zgłoszenie wraz z podstawowymi informacjami.</li>
          <li><strong>Weryfikacja i rekomendacja</strong> – zespół Investio ocenia projekt pod kątem merytorycznym i formalnym.</li>
          <li><strong>Publikacja i zbiórka</strong> – zweryfikowane projekty trafiają na platformę, gdzie inwestorzy mogą deklarować zainteresowanie.</li>
          <li><strong>Realizacja i monitoring</strong> – po zakończeniu zbiórki organizator realizuje projekt, a inwestorzy mają wgląd w postępy.</li>
        </ol>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Przejrzystość i bezpieczeństwo</h2>
        <p className="text-gray-700">
          Przed podjęciem decyzji inwestorzy mają dostęp do kluczowych informacji o projekcie: opisu biznesowego,
          harmonogramu, szacunkowego budżetu oraz zidentyfikowanych ryzyk. W przypadku projektów inwestycyjnych
          zapewniamy możliwość monitorowania ich postępów na bieżąco.
        </p>
        <p className="text-gray-700">
          Ta platforma nie przyjmuje płatności, wpłat ani inwestycji. Deklaracje zainteresowania nie są zobowiązaniem finansowym.
          Więcej informacji znajdziesz w sekcjach{" "}
          <a href="/ryzyka" className="underline hover:text-gray-900">Ryzyka</a> oraz{" "}
          <a href="/faq" className="underline hover:text-gray-900">FAQ</a>.
        </p>
      </section>

      <section className="space-y-6">
        <h2 className="text-2xl font-bold">Nasz zespół</h2>
        <p className="text-gray-700">
          Investio tworzą doświadczeni specjaliści z zakresu finansów, prawa i zarządzania projektami.
        </p>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <TeamMember
            name="John Smith"
            role="Chief Executive Officer (CEO)"
            email="john.smith@investio.pl"
            bio="John odpowiada za strategię rozwoju Investio. Wcześniej kierował zespołami produktowymi w branży fintech."
            photoSrc="/team/placeholder-1.jpg"
          />
          <TeamMember
            name="Anita Lockers"
            role="Chief Operating Officer (COO)"
            email="anita.lockers@investio.pl"
            bio="Anita nadzoruje codzienne operacje platformy oraz relacje z organizatorami projektów."
            photoSrc="/team/placeholder-2.jpg"
          />
          <TeamMember
            name="Michael Chen"
            role="Chief Technology Officer (CTO)"
            email="michael.chen@investio.pl"
            bio="Michael prowadzi zespół technologiczny Investio. Odpowiada za architekturę platformy i bezpieczeństwo danych."
            photoSrc="/team/placeholder-3.jpg"
          />
          <TeamMember
            name="Sarah Williams"
            role="Head of Investor Relations"
            email="sarah.williams@investio.pl"
            bio="Sarah dba o relacje z inwestorami i transparentność komunikacji na platformie."
            photoSrc="/team/placeholder-4.jpg"
          />
          <TeamMember
            name="David Miller"
            role="Legal Counsel"
            email="david.miller@investio.pl"
            bio="David nadzoruje zgodność prawną platformy z obowiązującymi regulacjami."
            photoSrc="/team/placeholder-5.jpg"
          />
          <TeamMember
            name="Emma Brown"
            role="Head of Project Verification"
            email="emma.brown@investio.pl"
            bio="Emma kieruje procesem weryfikacji projektów przed publikacją."
            photoSrc="/team/placeholder-6.jpg"
          />
        </div>

        <p className="text-sm text-gray-500">
          To jest szablon sekcji zespołu. Edytuj plik page.tsx i uzupełnij komponenty TeamMember prawdziwymi danymi.
        </p>
      </section>

      <section className="space-y-6">
        <h2 className="text-2xl font-bold">Rada Nadzorcza</h2>
        <p className="text-gray-700">
          Nadzór nad działalnością Investio sprawuje Rada Nadzorcza, w której skład wchodzą niezależni eksperci.
        </p>

        <div className="grid gap-6 sm:grid-cols-3">
          <BoardMember
            name="Robert Johnson"
            role="Przewodniczący Rady Nadzorczej"
            bio="Robert to były dyrektor zarządzający w instytucji finansowej z ponad 20-letnim doświadczeniem."
            photoSrc="/team/board-1.jpg"
          />
          <BoardMember
            name="Patricia Davis"
            role="Członek Rady Nadzorczej"
            bio="Patricia specjalizuje się w zarządzaniu ryzykiem i compliance w sektorze fintech."
            photoSrc="/team/board-2.jpg"
          />
          <BoardMember
            name="Thomas Wilson"
            role="Członek Rady Nadzorczej"
            bio="Thomas ma doświadczenie w private equity i venture capital."
            photoSrc="/team/board-3.jpg"
          />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Bibliografia / Źródła</h2>
        <p className="text-gray-700">
          Poniżej znajdziesz miejsce na bibliografię i źródła, z których korzystaliśmy przy tworzeniu Investio.
        </p>
        <ul className="list-disc list-inside space-y-1 text-gray-700">
          <li>[Miejsce na źródło 1 – np. ustawa o crowdfundingu, raport NBP, itp.]</li>
          <li>[Miejsce na źródło 2]</li>
          <li>[Miejsce na źródło 3]</li>
        </ul>
      </section>
    </div>
  );
}

function TeamMember({
  name,
  role,
  email,
  bio,
  photoSrc,
}: {
  name: string;
  role: string;
  email: string;
  bio: string;
  photoSrc: string;
}) {
  return (
    <div className="flex flex-col items-center text-center rounded border border-gray-200 bg-white p-6 shadow-sm">
      <div className="relative mb-4 h-32 w-32 overflow-hidden rounded-full bg-gray-100">
        <div className="flex h-full w-full items-center justify-center text-gray-400">
          brak zdjęcia
        </div>
      </div>
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="text-sm font-medium text-gray-600">{role}</p>
      <p className="mt-3 text-sm text-gray-700">{bio}</p>
      <a href={`mailto:${email}`} className="mt-4 inline-block text-sm text-blue-600 underline hover:text-blue-800">
        {email}
      </a>
    </div>
  );
}

function BoardMember({
  name,
  role,
  bio,
  photoSrc,
}: {
  name: string;
  role: string;
  bio: string;
  photoSrc: string;
}) {
  return (
    <div className="flex flex-col items-center text-center rounded border border-gray-200 bg-white p-6 shadow-sm">
      <div className="relative mb-4 h-32 w-32 overflow-hidden rounded-full bg-gray-100">
        <div className="flex h-full w-full items-center justify-center text-gray-400">
          brak zdjęcia
        </div>
      </div>
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="text-sm font-medium text-gray-600">{role}</p>
      <p className="mt-3 text-sm text-gray-700">{bio}</p>
    </div>
  );
}
