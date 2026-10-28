import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { smartSearch } from "../api";
import { useDocumentTitle } from "../hooks";
import PackageCard from "../components/PackageCard";
import SearchBox from "../components/SearchBox";
import WhatsAppButton from "../components/WhatsAppButton";

const EXAMPLES = ["relaxing beach holiday", "adventure with friends", "easy trip for my parents"];

function badgeFor(match, budget) {
  if (!budget || match.within_budget === null || match.within_budget === undefined) return null;
  return match.within_budget ? { text: "Within your budget", tone: "ok" } : { text: "Above your budget", tone: "warn" };
}

export default function Search() {
  useDocumentTitle("Smart search", "Search holidays by feeling and budget instead of place names.");
  const [params, setParams] = useSearchParams();
  const q = params.get("q") || "";
  const budget = params.get("budget") || "";
  const [state, setState] = useState({ status: "idle" });

  useEffect(() => {
    if (!q && !budget) { setState((s) => (s.status === "empty" ? s : { status: "idle" })); return; }
    let cancelled = false;
    setState({ status: "loading" });
    smartSearch({ query: q, budget: budget ? Number(budget) : null })
      .then((d) => !cancelled && setState({ status: "done", ...d }))
      .catch((ex) => !cancelled && setState({ status: "error", code: ex.status }));
    return () => { cancelled = true; };
  }, [q, budget]);

  const search = (nextQ, nextBudget) => {
    if (!nextQ && !nextBudget) return setState({ status: "empty" });
    const p = new URLSearchParams();
    if (nextQ) p.set("q", nextQ);
    if (nextBudget) p.set("budget", nextBudget);
    setParams(p);
  };

  const whatsappMsg = `Hi ASI Holidays, I'm looking for: ${q || "a holiday"}${budget ? ` (budget up to ₹${budget} per person)` : ""}`;

  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">Smart search</h1>
        <p className="lead-dark">Search by feeling and budget. No need to know exact place names. Write in any language.</p>

        <SearchBox key={`${q}|${budget}`} initialQuery={q} initialBudget={budget} onSearch={search} busy={state.status === "loading"} />
        <div className="chips">
          {EXAMPLES.map((x) => <button key={x} type="button" className="chip" onClick={() => search(x, budget)}>{x}</button>)}
        </div>

        {state.status === "empty" && <p className="err">Type what you are looking for or choose a budget.</p>}
        {state.status === "error" && (
          <p className="err">
            {state.code === 429 ? "You have searched a lot. Please try again later or chat with us on WhatsApp."
              : state.code === 400 ? "Please type what you are looking for or choose a budget."
              : "Search is not available right now. Please try again."}
          </p>
        )}

        {state.status === "done" && (
          <>
            {state.intro && <p className="lead-dark">{state.intro}</p>}
            {state.budget?.note && <div className="note" role="note">{state.budget.note}</div>}

            {state.matches.length > 0 ? (
              <div className="grid">
                {state.matches.map((m) => <PackageCard key={m.package.slug} pkg={m.package} reason={m.reason} badge={badgeFor(m, state.budget)} />)}
              </div>
            ) : (
              <WhatsAppButton label="Tell a consultant what you want" message={whatsappMsg} />
            )}

            {state.budget?.alternatives?.length > 0 && (
              <>
                <h2 className="h3">Closer to your budget</h2>
                <div className="grid">
                  {state.budget.alternatives.map((m) => <PackageCard key={m.package.slug} pkg={m.package} reason={m.reason} badge={badgeFor(m, state.budget)} />)}
                </div>
              </>
            )}
          </>
        )}
        <p className="fine">Only approved ASI packages are shown. Prices are indicative; a consultant confirms every quote.</p>
      </div>
    </section>
  );
}