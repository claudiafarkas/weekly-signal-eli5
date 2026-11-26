import { SubscribeForm } from "@/components/SubscribeForm";

const SECTIONS = [
  ["The Big Story", "The one development that defined the week."],
  ["AI & Technology", "Models, software, and the tools people are building with."],
  ["Data & Engineering", "Pipelines, databases, cloud, and how systems are put together."],
  ["Business & Markets", "Companies, capital, and shifts that change the industry."],
  ["Beyond the Tech Bubble", "Economics and events that explain the wider picture."],
  ["Connecting the Dots", "A link between two stories, when one is actually there."],
  ["The 5-Minute Deep Dive", "One idea from the week, taught properly."],
] as const;

export default function HomePage() {
  return (
    <main className="page">
      <header className="masthead">
        <span>A Sunday letter</span>
        <span>Next issue · {nextIssueLabel()}</span>
      </header>

      <h1 className="wordmark">The Weekly Signal</h1>
      <p className="tagline">Less noise. More signal.</p>
      <p className="deck">
        The news in technology, data, and business, read through the week and
        reduced to what is worth understanding. Complicated ideas, explained
        in plain language.
      </p>

      <SubscribeForm />

      <hr className="rule" />

      <section aria-labelledby="anatomy-heading">
        <h2 id="anatomy-heading" className="section-kicker">
          How a story is told
        </h2>
        <dl className="anatomy">
          <div>
            <dt>What happened</dt>
            <dd>The facts, short enough to read once.</dd>
          </div>
          <div>
            <dt>Explain it simply</dt>
            <dd>The idea, without assuming you already know the term.</dd>
          </div>
          <div>
            <dt>Why it matters</dt>
            <dd>Who it affects, and what is still unsettled.</dd>
          </div>
        </dl>
      </section>

      <hr className="rule" />

      <section aria-labelledby="sections-heading">
        <h2 id="sections-heading" className="section-kicker">
          In the letter, when the week earns it
        </h2>
        <ul className="sections">
          {SECTIONS.map(([title, detail]) => (
            <li key={title}>
              {title}
              <span>{detail}</span>
            </li>
          ))}
        </ul>
      </section>

      <footer className="footer">
        <span>The Weekly Signal</span>
        <span>Less noise. More signal.</span>
      </footer>
    </main>
  );
}

function nextIssueLabel(now = new Date()): string {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    weekday: "short",
  }).formatToParts(now);

  const value = (type: string) => parts.find((part) => part.type === type)?.value ?? "";
  const weekdayIndex: Record<string, number> = {
    Sun: 0,
    Mon: 1,
    Tue: 2,
    Wed: 3,
    Thu: 4,
    Fri: 5,
    Sat: 6,
  };
  const daysUntilSunday = (7 - (weekdayIndex[value("weekday")] ?? 0)) % 7;
  const issue = new Date(
    Date.UTC(Number(value("year")), Number(value("month")) - 1, Number(value("day")) + daysUntilSunday),
  );

  return new Intl.DateTimeFormat("en-GB", {
    timeZone: "UTC",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(issue);
}
