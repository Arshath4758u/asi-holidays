import { useEffect, useState } from "react";
import { getPackages } from "../api";
import PackageCard from "../components/PackageCard";

const CATEGORIES = [
  ["", "All"], ["india", "India"], ["international", "International"],
  ["family", "Family"], ["honeymoon", "Honeymoon"], ["group", "Group tours"], ["custom", "Customised"],
];

export default function Packages() {
  const [category, setCategory] = useState("");
  const [items, setItems] = useState([]);
  useEffect(() => {
    getPackages(category ? { category } : {}).then(setItems).catch(() => setItems([]));
  }, [category]);
  return (
    <section>
      <h2>Holiday packages</h2>
      <div className="chips">
        {CATEGORIES.map(([v, l]) => (
          <button key={v} className={v === category ? "chip on" : "chip"} onClick={() => setCategory(v)}>{l}</button>
        ))}
      </div>
      <div className="grid">{items.map((p) => <PackageCard key={p.id} pkg={p} />)}</div>
      {items.length === 0 && <p>No packages found.</p>}
    </section>
  );
}
