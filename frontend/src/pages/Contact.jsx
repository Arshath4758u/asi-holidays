import { useSearchParams } from "react-router-dom";
import { useDocumentTitle } from "../hooks";
import { useSite } from "../site";
import EnquiryForm from "../components/EnquiryForm";
import WhatsAppButton from "../components/WhatsAppButton";

export default function Contact() {
  useDocumentTitle("Contact us", "Tell us about your trip. A consultant will get back to you.");
  const s = useSite();
  const [params] = useSearchParams();
  const defaults = { destination: params.get("destination") || "", travel_month: params.get("month") || "", travellers: params.get("travellers") || 2 };

  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">Contact us</h1>
        <p className="lead-dark">Tell us about your trip. A consultant will get back to you.</p>
        <div className="layout-contact">
          <div className="side-card">
            <h2 className="h3">Send us an enquiry</h2>
            <EnquiryForm variant="full" defaults={defaults} />
          </div>
          <div>
            <div className="side-card">
              <h2 className="h3">Contact details</h2>
              {s.phone_display && <p>{s.phone_display}</p>}
              {s.email && <p>{s.email}</p>}
              {s.address && <p>{s.address}</p>}
              {s.opening_hours && <p>{s.opening_hours}</p>}
            </div>
            <WhatsAppButton variant="gold" className="btn-block gap" label="Chat on WhatsApp" message="Hi ASI Holidays, I have a question." />
            {s.address && (
              <iframe
                className="map"
                title="Office location"
                loading="lazy"
                src={`https://maps.google.com/maps?q=${encodeURIComponent(s.address)}&output=embed`}
              />
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
