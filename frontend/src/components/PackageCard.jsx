import { Link } from "react-router-dom";

export default function PackageCard({ pkg }) {
  return (
    <Link to={`/packages/${pkg.slug}`} className="card">
      {pkg.image ? <img src={pkg.image} alt={pkg.title} loading="lazy" /> : <div className="card-ph" />}
      <div className="card-body">
        <span className="tag">{pkg.category_label}</span>
        <h3>{pkg.title}</h3>
        <p>{pkg.summary}</p>
        <p className="price">
          {pkg.duration_days} days · from ₹{Number(pkg.price_from).toLocaleString("en-IN")} / person
        </p>
      </div>
    </Link>
  );
}
