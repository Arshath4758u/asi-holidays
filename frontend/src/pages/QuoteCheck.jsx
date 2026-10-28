import { useEffect, useState } from "react";
import { getPackages, submitQuoteCheck } from "../api";
import { useDocumentTitle } from "../hooks";

export default function QuoteCheck() {
  useDocumentTitle("Check my quote", "Share another agency's quote. A consultant compares it line by line.");
  const [packages, setPackages] = useState([]);
  const [form, setForm] = useState({ name: "", whatsapp_number: "", package_slug: "", quote_text: "", consent_followup: false, website: "" });
  const [state, setState] = useState({ status: "idle", errors: {} });

  useEffect(() => { getPackages().then(setPackages).catch(() => {}); }, []);
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.type === "checkbox" ? e.target.checked : e.target.value });
  const err = (k) => state.errors[k] && <small className="err">{[].concat(state.errors[k]).join(" ")}</small>;

  const submit = async (e) => {
    e.preventDefault();
    setState({ status: "sending", errors: {} });
    try {
      await submitQuoteCheck(form);
      setState({ status: "done", errors: {} });
    } catch (ex) {
      setState({ status: "error", errors: ex.data || {}, code: ex.status });
    }
  };

  if (state.status === "done") {
    return (
      <section className="section"><div className="wrap narrow center">
        <div className="tick">✓</div>
        <h1 className="h2">We have your quote</h1>
        <p className="lead-dark">A consultant will review it and send you a line-by-line comparison on WhatsApp.</p>
      </div></section>
    );
  }

  return (
    <section className="section">
      <div className="wrap narrow">
        <h1 className="h2">Check my quote</h1>
        <p className="lead-dark">Got another agency's quote? Paste it here. A consultant compares it with ours, line by line, and replies on WhatsApp.</p>
        <form className="form" onSubmit={submit}>
          <div className="row">
            <label>Your name<input required value={form.name} onChange={set("name")} />{err("name")}</label>
            <label>Phone / WhatsApp<input required inputMode="tel" value={form.whatsapp_number} onChange={set("whatsapp_number")} placeholder="+91" />{err("whatsapp_number")}</label>
          </div>
          <label>Compare with (optional)
            <select value={form.package_slug} onChange={set("package_slug")}>
              <option value="">No specific package</option>
              {packages.map((p) => <option key={p.slug} value={p.slug}>{p.title}</option>)}
            </select>
          </label>
          <label>The other agency's quote<textarea required rows="8" value={form.quote_text} onChange={set("quote_text")} placeholder="Paste the hotels, meals, transfers, sightseeing and total price here" />{err("quote_text")}</label>
          <input className="hp" tabIndex="-1" autoComplete="off" aria-hidden="true" value={form.website} onChange={set("website")} name="website" />
          <label className="check"><input type="checkbox" checked={form.consent_followup} onChange={set("consent_followup")} /><span>I agree to be contacted about this quote.</span></label>
          {err("consent_followup")}
          {state.status === "error" && <small className="err">{state.code === 429 ? "Too many requests from this device. Please try again later." : "Could not send. Please check the fields."}</small>}
          <button className="btn btn-gold" disabled={state.status === "sending"}>{state.status === "sending" ? "Sending..." : "Send for review"}</button>
        </form>
        <p className="fine">Do not paste card numbers or passport details.</p>
      </div>
    </section>
  );
}