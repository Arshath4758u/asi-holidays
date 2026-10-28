import { Link } from "react-router-dom";
import { useDocumentTitle } from "../hooks";
import { useSite } from "../site";

const OFFER = ["India holidays", "International tours", "Family holidays", "Honeymoon packages", "Group tours", "Custom itineraries", "Corporate travel"];

export default function About() {
  useDocumentTitle("About us", "ASI Holidays plans personal holidays across India and abroad.");
  const s = useSite();
  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">About ASI Holidays</h1>
        <p className="lead-dark">A travel business that plans personal holidays across India and abroad.</p>
        <div className="about-grid">
          <p>{s.about_text}</p>
          <div className="ph tall">Team or office photo</div>
        </div>
        <div className="mission">
          <p className="eyebrow">Our mission</p>
          <p className="mission-text">{s.mission}</p>
        </div>
        <h2 className="h3">What we offer</h2>
        <div className="offer">{OFFER.map((o) => <div key={o}>{o}</div>)}</div>
        <div className="cta">
          <h2>Ready to plan your holiday?</h2>
          <Link className="btn btn-navy" to="/contact">Get a free quote</Link>
        </div>
      </div>
    </section>
  );
}
