import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { getPackage } from "../api";
import { rupees, useDocumentTitle } from "../hooks";
import EnquiryForm from "../components/EnquiryForm";
import WhatsAppButton from "../components/WhatsAppButton";

const stripDay = (line) => line.replace(/^day\s*\d+\s*[:\-–.]?\s*/i, "");

export default function PackageDetail() {
  const { slug } = useParams();
  const { hash } = useLocation();
  const [pkg, setPkg] = useState(null);
  const [missing, setMissing] = useState(false);

  useDocumentTitle(pkg?.title, pkg?.summary);

  useEffect(() => {
    setPkg(null);
    setMissing(false);
    getPackage(slug).then(setPkg).catch(() => setMissing(true));
  }, [slug]);

  useEffect(() => {
    if (pkg && hash === "#enquire") document.getElementById("enquire")?.scrollIntoView({ behavior: "smooth" });
  }, [pkg, hash]);

  if (missing) return <div className="wrap section"><p>Package not found. <Link className="link" to="/packages">See all packages</Link></p></div>;
  if (!pkg) return <div className="wrap section"><p>Loading...</p></div>;

  const msg = `Hi ASI Holidays, I'm interested in "${pkg.title}". Please share details.`;

  return (
    <section className="section">
      <div className="wrap">
        <p className="crumbs"><Link to="/">Home</Link> / <Link to={`/packages?region=${pkg.region}`}>{pkg.region_label} holidays</Link> / {pkg.title}</p>
        <h1 className="h2">{pkg.title}</h1>
        <p className="meta big">{pkg.duration_days} days · from ₹{rupees(pkg.price_from)} per person</p>
        <div className="layout-detail">
          <div>
            {pkg.image ? <img className="detail-img" src={pkg.image} alt={pkg.title} /> : <div className="ph detail-img">Photo coming soon</div>}
            <p>{pkg.summary}</p>
            {pkg.itinerary.length > 0 && (
              <>
                <h2 className="h3">Itinerary</h2>
                {pkg.itinerary.map((d, i) => (
                  <div className="day" key={i}><strong>Day {i + 1}</strong><span>{stripDay(d)}</span></div>
                ))}
              </>
            )}
            {pkg.inclusions.length > 0 && (<><h2 className="h3">What is included</h2><ul>{pkg.inclusions.map((d, i) => <li key={i}>{d}</li>)}</ul></>)}
            {pkg.exclusions.length > 0 && (<><h2 className="h3">Not included</h2><ul>{pkg.exclusions.map((d, i) => <li key={i}>{d}</li>)}</ul></>)}
          </div>
          <aside className="side-card" id="enquire">
            <h2 className="h3">Enquire about this trip</h2>
            <EnquiryForm variant="compact" packageSlug={pkg.slug} defaults={{ destination: pkg.destination }} />
            <WhatsAppButton variant="outline" className="btn-block" packageSlug={pkg.slug} label="Chat on WhatsApp" message={msg} />
          </aside>
        </div>
      </div>
    </section>
  );
}
