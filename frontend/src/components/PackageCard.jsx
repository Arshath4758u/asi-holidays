import { Link } from "react-router-dom";
import { rupees } from "../hooks";

export default function PackageCard({ pkg }) {
  return (
    <article className="card">
      <Link to={`/packages/${pkg.slug}`} className="card-link">
        {pkg.image ? <img src={pkg.image} alt={pkg.title} loading="lazy" /> : <div className="ph">Photo coming soon</div>}
        <div className="card-body">
          <h3>{pkg.title}</h3>
          <p className="meta">{pkg.duration_days} days · from ₹{rupees(pkg.price_from)} per person</p>
          <p className="sum">{pkg.summary}</p>
        </div>
      </Link>
      <Link className="btn btn-gold btn-block" to={`/packages/${pkg.slug}#enquire`}>Enquire now</Link>
    </article>
  );
}