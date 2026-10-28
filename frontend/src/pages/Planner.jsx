import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { planTrip } from "../api";
import { useDocumentTitle } from "../hooks";
import PackageCard from "../components/PackageCard";
import WhatsAppButton from "../components/WhatsAppButton";

const EXAMPLES = ["5 days in Kerala for 4", "Honeymoon, Europe, May", "Long weekend near Chennai"];

export default function Planner() {
  useDocumentTitle("AI trip planner", "Describe your trip in one line and see matching ASI Holidays packages.");
  const [params] = useSearchParams();
  const [query, setQuery] = useState(params.get("q") || "");
  const [state, setState] = useState({ status: "idle" });

  const run = async (q) => {
    setState({ status: "loading" });
    try {
      setState({ status: "done", ...(await planTrip(q)) });
    } catch (ex) {
      setState({ status: "error", code: ex.status });
    }
  };

  useEffect(() => { if (params.get("q")) run(params.get("q")); }, []);

  const onSubmit = (e) => { e.preventDefault(); if (query.trim().length >= 3) run(query.trim()); };

  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">AI trip planner</h1>
        <p className="lead-dark">Describe your trip in one line and see matching packages. Write in any language.</p>
        <form className="planner" onSubmit={onSubmit}>
          <input value={query} onChange={(e) => setQuery(e.target.value)} maxLength={300} placeholder="5 days in Kerala for a family of 4 in December" aria-label="Describe your trip" />
          <button className="btn btn-gold" disabled={state.status === "loading"}>{state.status === "loading" ? "Planning..." : "Plan my trip"}</button>
        </form>
        <div className="chips">
          {EXAMPLES.map((x) => <button key={x} className="chip" type="button" onClick={() => { setQuery(x); run(x); }}>{x}</button>)}
        </div>

        {state.status === "error" && <p className="err">{state.code === 429 ? "You have used the planner a lot. Please try again later or chat with us on WhatsApp." : "Something went wrong. Please try again."}</p>}
        {state.status === "done" && (
          <>
            <p className="lead-dark">{state.intro}</p>
            {state.matches.length > 0 ? (
              <div className="grid">{state.matches.map((m) => <PackageCard key={m.package.slug} pkg={m.package} reason={m.reason} />)}</div>
            ) : (
              <WhatsAppButton label="Plan it with a consultant on WhatsApp" message={`Hi ASI Holidays, I'd like help with this trip: ${query}`} />
            )}
          </>
        )}
        <p className="fine">Only approved ASI packages are shown. A consultant confirms every quote.</p>
      </div>
    </section>
  );
}