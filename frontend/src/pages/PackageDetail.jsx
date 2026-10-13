import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPackage } from "../api";
import EnquiryForm from "../components/EnquiryForm";
import WhatsAppButton from "../components/WhatsAppButton";

export default function PackageDetail() {
  const { slug } = useParams();
  const [pkg, setPkg] = useState(null);
  const [missing, setMissing] = useState(false);

  useEffect(() => {
    setPkg(null);
    getPackage(slug).then((p) => { setPkg(p); document.title = `${p.title} | ASI Holidays`; }).catch(() => setMissing(true));
  }, [slug]);

  if (missing) return <p>Package not found.</p>;
  if (!pkg) return <p>Loading...</p>;

  return (
    <article>
      {pkg.image && <img className="detail-img" src={pkg.image} alt={pkg.title} />}
      <h1>{pkg.title}</h1>
      <p className="price">{pkg.duration_days} days · from ₹{Number(pkg.price_from).toLocaleString("en-IN")} / person</p>
      <p>{pkg.summary}</p>
      <WhatsAppButton
        packageSlug={pkg.slug}
        message={`Hi ASI Holidays, I'm interested in "${pkg.title}". Please share details.`}
      />
      {pkg.itinerary.length > 0 && (<><h2>Itinerary</h2><ol>{pkg.itinerary.map((d, i) => <li key={i}>{d}</li>)}</ol></>)}
      {pkg.inclusions.length > 0 && (<><h2>Inclusions</h2><ul>{pkg.inclusions.map((d, i) => <li key={i}>{d}</li>)}</ul></>)}
      {pkg.exclusions.length > 0 && (<><h2>Exclusions</h2><ul>{pkg.exclusions.map((d, i) => <li key={i}>{d}</li>)}</ul></>)}
      <h2>Send an enquiry</h2>
      <EnquiryForm packageSlug={pkg.slug} defaultDestination={pkg.destination} />
    </article>
  );
}
