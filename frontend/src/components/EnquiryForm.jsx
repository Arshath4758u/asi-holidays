import { useState } from "react";
import { submitEnquiry } from "../api";

const empty = {
  name: "", whatsapp_number: "", destination: "", departure_date: "",
  travellers: 2, budget: "", message: "", consent_followup: true, website: "",
};

export default function EnquiryForm({ packageSlug = "", defaultDestination = "" }) {
  const [form, setForm] = useState({ ...empty, destination: defaultDestination });
  const [state, setState] = useState({ status: "idle", errors: {} });

  const set = (k) => (e) =>
    setForm({ ...form, [k]: e.target.type === "checkbox" ? e.target.checked : e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setState({ status: "sending", errors: {} });
    const body = { ...form, package_slug: packageSlug };
    if (!body.departure_date) delete body.departure_date;
    try {
      await submitEnquiry(body);
      setState({ status: "done", errors: {} });
      setForm({ ...empty, destination: defaultDestination });
    } catch (err) {
      setState({ status: "error", errors: err.data || {} });
    }
  };

  if (state.status === "done")
    return <p className="notice">Thank you. Our travel consultant will contact you on WhatsApp shortly.</p>;

  const err = (k) => state.errors[k] && <small className="err">{[].concat(state.errors[k]).join(" ")}</small>;

  return (
    <form className="form" onSubmit={onSubmit}>
      <label>Name<input required value={form.name} onChange={set("name")} />{err("name")}</label>
      <label>WhatsApp number<input required inputMode="tel" value={form.whatsapp_number} onChange={set("whatsapp_number")} />{err("whatsapp_number")}</label>
      <label>Destination<input value={form.destination} onChange={set("destination")} /></label>
      <label>Departure date<input type="date" value={form.departure_date} onChange={set("departure_date")} />{err("departure_date")}</label>
      <label>Travellers<input type="number" min="1" value={form.travellers} onChange={set("travellers")} /></label>
      <label>Budget (per person)<input value={form.budget} onChange={set("budget")} placeholder="e.g. 50,000 - 70,000" /></label>
      <label>Message<textarea rows="3" value={form.message} onChange={set("message")} /></label>
      {/* honeypot: hidden from people, bots fill it */}
      <input className="hp" tabIndex="-1" autoComplete="off" aria-hidden="true" value={form.website} onChange={set("website")} />
      <label className="check">
        <input type="checkbox" checked={form.consent_followup} onChange={set("consent_followup")} />
        I agree to be contacted on WhatsApp about this enquiry.
      </label>
      {state.status === "error" && <small className="err">Could not send. Please check the fields or try WhatsApp.</small>}
      <button disabled={state.status === "sending"}>{state.status === "sending" ? "Sending..." : "Send enquiry"}</button>
    </form>
  );
}
