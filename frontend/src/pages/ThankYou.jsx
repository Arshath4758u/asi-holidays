import { Link, useLocation } from "react-router-dom";
import { useDocumentTitle } from "../hooks";
import { useSite } from "../site";
import WhatsAppButton from "../components/WhatsAppButton";

export default function ThankYou() {
  useDocumentTitle("Thank you");
  const { state } = useLocation();
  const s = useSite();
  const name = state?.name;
  return (
    <section className="section">
      <div className="wrap center">
        <div className="tick">✓</div>
        <h1 className="h2">Thank you{name ? `, ${name}` : ""}</h1>
        <p className="lead-dark">Your enquiry is received. A consultant will contact you on WhatsApp within {s.response_time}.</p>
        <div className="actions">
          <WhatsAppButton variant="gold" label="Chat on WhatsApp" message="Hi ASI Holidays, I just sent an enquiry on your website." />
          <Link className="btn btn-outline" to="/packages">Browse packages</Link>
        </div>
        <div className="steps">
          <div className="step"><small>Step 1</small><h3>We review</h3><p>A consultant reads your enquiry.</p></div>
          <div className="step"><small>Step 2</small><h3>We plan</h3><p>You get a quote we have checked.</p></div>
          <div className="step"><small>Step 3</small><h3>You decide</h3><p>Confirm when you are happy.</p></div>
        </div>
      </div>
    </section>
  );
}
