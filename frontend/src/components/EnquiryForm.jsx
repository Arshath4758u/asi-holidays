import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { submitEnquiry } from "../api";
import { trackEvent } from "../analytics";

// variant "compact": package page sidebar. variant "full": contact page.
export default function EnquiryForm({ variant = "full", packageSlug = "", defaults = {} }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "", whatsapp_number: "", email: "", destination: defaults.destination || "",
    departure_date: "", travel_month: defaults.travel_month || "",
    travellers: defaults.travellers || 2, message: "", consent_followup: false, website: "",
  });
  const [state, setState] = useState({ status: "idle", errors: {} });
  const compact = variant === "compact";

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.type === "checkbox" ? e.target.checked : e.target.value });
  const err = (k) => state.errors[k] && <small className="err">{[].concat(state.errors[k]).join(" ")}</small>;

  const onSubmit = async (e) => {
    e.preventDefault();
    setState({ status: "sending", errors: {} });
    const source = compact ? "package_form" : "contact_form";
    const body = { ...form, travellers: Number(form.travellers) || 1, package_slug: packageSlug, source };
    if (!body.departure_date) delete body.departure_date;
    try {
      await submitEnquiry(body);
      trackEvent("generate_lead", { source, package: packageSlug });
      navigate("/thank-you", { state: { name: form.name.split(" ")[0] } });
    } catch (ex) {
      setState({ status: "error", errors: ex.data || {}, code: ex.status });
    }
  };

  return (
    <form className="form" onSubmit={onSubmit} noValidate={false}>
      <div className={compact ? "" : "row"}>
        <label>Your name<input required value={form.name} onChange={set("name")} placeholder="Your name" />{err("name")}</label>
        <label>Phone / WhatsApp<input required inputMode="tel" value={form.whatsapp_number} onChange={set("whatsapp_number")} placeholder="+91" />{err("whatsapp_number")}</label>
      </div>
      {!compact && (
        <label>Email<input type="email" value={form.email} onChange={set("email")} placeholder="you@example.com" />{err("email")}</label>
      )}
      {compact ? (
        <label>Travel date<input type="date" value={form.departure_date} onChange={set("departure_date")} />{err("departure_date")}</label>
      ) : (
        <div className="row3">
          <label>Destination<input value={form.destination} onChange={set("destination")} placeholder="e.g. Kerala" /></label>
          <label>Travel month<input value={form.travel_month} onChange={set("travel_month")} placeholder="e.g. December" /></label>
          <label>Travellers<input type="number" min="1" value={form.travellers} onChange={set("travellers")} />{err("travellers")}</label>
        </div>
      )}
      {compact && (
        <label>Travellers<input type="number" min="1" value={form.travellers} onChange={set("travellers")} placeholder="e.g. 4" />{err("travellers")}</label>
      )}
      {!compact && (
        <label>Message<textarea rows="3" value={form.message} onChange={set("message")} placeholder="Tell us about your trip" /></label>
      )}
      {/* honeypot: hidden from people, bots fill it */}
      <input className="hp" tabIndex="-1" autoComplete="off" aria-hidden="true" value={form.website} onChange={set("website")} name="website" />
      <label className="check">
        <input type="checkbox" checked={form.consent_followup} onChange={set("consent_followup")} />
        <span>I agree to be contacted about this enquiry.</span>
      </label>
      {err("consent_followup")}
      {state.status === "error" && (
        <small className="err">
          {state.code === 429 ? "Too many enquiries from this device. Please use the WhatsApp button." : "Could not send. Please check the highlighted fields or use WhatsApp."}
        </small>
      )}
      <button className="btn btn-gold btn-block" disabled={state.status === "sending"}>
        {state.status === "sending" ? "Sending..." : "Send enquiry"}
      </button>
    </form>
  );
}