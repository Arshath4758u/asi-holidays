import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getPackages } from "../api";
import PackageCard from "../components/PackageCard";
import WhatsAppButton from "../components/WhatsAppButton";

export default function Home() {
  const [featured, setFeatured] = useState([]);
  useEffect(() => { getPackages({ featured: "1" }).then(setFeatured).catch(() => {}); }, []);
  return (
    <>
      <section className="hero">
        <h1>Holidays planned around you</h1>
        <p>India and international packages, family trips, honeymoons and group tours.</p>
        <WhatsAppButton message="Hi ASI Holidays, I'd like help planning a holiday." />
        <Link to="/packages" className="link">Browse all packages</Link>
      </section>
      <section>
        <h2>Featured holidays</h2>
        <div className="grid">{featured.map((p) => <PackageCard key={p.id} pkg={p} />)}</div>
      </section>
    </>
  );
}
