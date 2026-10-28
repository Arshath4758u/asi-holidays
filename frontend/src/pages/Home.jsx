import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getPackages } from "../api";
import { useDocumentTitle } from "../hooks";
import PackageCard from "../components/PackageCard";
import WhatsAppButton from "../components/WhatsAppButton";
import SearchBox from "../components/SearchBox";
const KINDS = [
  ["India holidays", "/packages?region=india"],
  ["International tours", "/packages?region=international"],
  ["Honeymoon packages", "/packages?category=honeymoon"],
  ["Family holidays", "/packages?category=family"],
  ["Group tours", "/packages?category=group"],
  ["Corporate travel", "/packages?category=corporate"],
];

export default function Home() {
  useDocumentTitle("", "Personal holiday planning across India and abroad for families, couples, groups and companies.");
  const navigate = useNavigate();
  const [popular, setPopular] = useState([]);
  const [q, setQ] = useState({ destination: "", month: "", travellers: "" });
  const [oneLine, setOneLine] = useState("");

  useEffect(() => {
    getPackages({ featured: "1" })
      .then((f) => (f.length ? setPopular(f.slice(0, 3)) : getPackages().then((a) => setPopular(a.slice(0, 3)))))
      .catch(() => {});
  }, []);

  const onSearch = (e) => {
    e.preventDefault();
    const p = new URLSearchParams();
    if (q.destination) p.set("destination", q.destination);
    if (q.month) p.set("month", q.month);
    if (q.travellers) p.set("travellers", q.travellers);
    navigate(`/contact?${p}`);
  };

  const onPlan = (e) => {
    e.preventDefault();
    if (oneLine.trim().length >= 3) navigate(`/plan?q=${encodeURIComponent(oneLine.trim())}`);
  };

  return (
    <>
      <section className="hero">
        <div className="wrap hero-grid">
          <div>
            <p className="eyebrow">Your global travel partner</p>
            <h1>Holidays planned personally, in your language.</h1>
            <p className="lead">India and abroad, for families, couples, groups and companies.</p>
            <form className="search" onSubmit={onSearch}>
              <label>Destination<input value={q.destination} onChange={(e) => setQ({ ...q, destination: e.target.value })} placeholder="e.g. Kerala" /></label>
              <label>Month<input value={q.month} onChange={(e) => setQ({ ...q, month: e.target.value })} placeholder="e.g. December" /></label>
              <label>Travellers<input type="number" min="1" value={q.travellers} onChange={(e) => setQ({ ...q, travellers: e.target.value })} placeholder="e.g. 4" /></label>
              <button className="btn btn-gold">Get a quote</button>
            </form>
          </div>
          <div className="hero-art" aria-hidden="true">
            <img src="/hero.jpg" alt="" onError={(e) => (e.currentTarget.style.display = "none")} />
          </div>
        </div>
      </section>

      <section className="trust">
        <div className="wrap trust-grid">
          <div><b>Personal service</b><span>Your holiday planned for you, not picked from a list.</span></div>
          <div><b>Any-language support</b><span>Message us on WhatsApp in your own language.</span></div>
          <div><b>Every quote checked</b><span>A consultant reviews each quote before it reaches you.</span></div>
        </div>
      </section>

      <section className="section">
        <div className="wrap">
          <h2>Find your kind of holiday</h2>
          <SearchBox />
          <div className="kinds">
            {KINDS.map(([label, to]) => (
              <Link key={label} to={to} className="kind"><div className="ph" /><h3>{label}</h3></Link>
            ))}
          </div>
        </div>
      </section>

      <section className="section alt">
        <div className="wrap">
          <h2>Popular packages</h2>
          {popular.length ? <div className="grid">{popular.map((p) => <PackageCard key={p.id} pkg={p} />)}</div> : <p>Packages coming soon.</p>}
          <p><Link to="/packages" className="link">Browse all packages</Link></p>
        </div>
      </section>

      <section className="band ai-band">
        <div className="wrap">
          <h2>Describe your trip in one line</h2>
          <p>Our AI trip planner shows matching packages. A consultant confirms every quote.</p>
          <form className="planner" onSubmit={onPlan}>
            <input value={oneLine} onChange={(e) => setOneLine(e.target.value)} placeholder="5 days in Kerala for a family of 4 in December" aria-label="Describe your trip" maxLength={300} />
            <button className="btn btn-gold">Plan my trip</button>
          </form>
        </div>
      </section>

      <section className="band">
        <div className="wrap band-row">
          <div>
            <h2>Plan your trip on WhatsApp</h2>
            <p>Message us in your own language. A consultant checks every quote before it reaches you.</p>
          </div>
          <WhatsAppButton variant="gold" label="Chat on WhatsApp" message="Hi ASI Holidays, I'd like to plan a trip." />
        </div>
      </section>
    </>
  );
}