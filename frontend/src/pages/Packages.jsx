import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getPackages } from "../api";
import { useDocumentTitle } from "../hooks";
import PackageCard from "../components/PackageCard";
import SearchBox from "../components/SearchBox";

const GROUPS = [
  { key: "region", title: "Where", options: [["india", "India"], ["international", "International"]] },
  { key: "category", title: "Trip type", options: [["honeymoon", "Honeymoon"], ["family", "Family"], ["group", "Group"], ["corporate", "Corporate"]] },
  { key: "food", title: "Food needs", options: [["veg", "Vegetarian"], ["jain", "Jain"], ["halal", "Halal"]] },
  { key: "with", title: "Travelling with", options: [["kids", "Kids"], ["seniors", "Seniors"]] },
];

export default function Packages() {
  useDocumentTitle("Holiday packages", "Browse approved ASI Holidays packages for India and international trips.");
  const [params, setParams] = useSearchParams();
  const [items, setItems] = useState(null);

  const selected = (key) => (params.get(key) || "").split(",").filter(Boolean);

  const toggle = (key, val) => {
    const cur = selected(key);
    const next = cur.includes(val) ? cur.filter((v) => v !== val) : [...cur, val];
    const p = new URLSearchParams(params);
    next.length ? p.set(key, next.join(",")) : p.delete(key);
    setParams(p);
  };

  useEffect(() => {
    setItems(null);
    getPackages(Object.fromEntries(params)).then(setItems).catch(() => setItems([]));
  }, [params]);

  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">Holiday packages</h1>
        <p className="lead-dark">Browse approved ASI Holidays packages, or tell us what you need.</p>
        <SearchBox />
        <div className="layout-filters">
          <aside className="filters">
            <h3>Filters</h3>
            {GROUPS.map((g) => (
              <fieldset key={g.key}>
                <legend>{g.title}</legend>
                {g.options.map(([val, label]) => (
                  <label key={val} className="check">
                    <input type="checkbox" checked={selected(g.key).includes(val)} onChange={() => toggle(g.key, val)} />
                    <span>{label}</span>
                  </label>
                ))}
              </fieldset>
            ))}
            {params.toString() && <button className="link-btn" onClick={() => setParams({})}>Clear filters</button>}
          </aside>
          <div>
            {items === null && <p>Loading...</p>}
            {items && items.length === 0 && <p>No packages match these filters. Try removing one, or <a className="link" href="/contact">tell us what you need</a>.</p>}
            {items && items.length > 0 && <div className="grid grid-2">{items.map((p) => <PackageCard key={p.id} pkg={p} />)}</div>}
          </div>
        </div>
      </div>
    </section>
  );
}
