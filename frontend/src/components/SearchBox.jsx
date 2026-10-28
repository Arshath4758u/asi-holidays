import { useState } from "react";
import { useNavigate } from "react-router-dom";

const BUDGETS = [
  ["", "Any budget"],
  ["15000", "Up to ₹15,000"],
  ["25000", "Up to ₹25,000"],
  ["40000", "Up to ₹40,000"],
  ["60000", "Up to ₹60,000"],
  ["100000", "Up to ₹1,00,000"],
];

// With an onSearch handler it just reports the values (Search page).
// Without one it opens /search with the values in the URL (Home and Packages pages).
export default function SearchBox({ initialQuery = "", initialBudget = "", onSearch, busy = false }) {
  const navigate = useNavigate();
  const [q, setQ] = useState(initialQuery);
  const [budget, setBudget] = useState(initialBudget);

  const submit = (e) => {
    e.preventDefault();
    if (onSearch) return onSearch(q.trim(), budget);
    const p = new URLSearchParams();
    if (q.trim()) p.set("q", q.trim());
    if (budget) p.set("budget", budget);
    navigate(`/search${p.toString() ? `?${p}` : ""}`);
  };

  return (
    <form className="searchbox" onSubmit={submit}>
      <label>What kind of trip?
        <input value={q} onChange={(e) => setQ(e.target.value)} maxLength={300} placeholder="e.g. relaxing, adventure, easy for my parents" />
      </label>
      <label>Budget per person
        <select value={budget} onChange={(e) => setBudget(e.target.value)}>
          {BUDGETS.map(([v, label]) => <option key={v} value={v}>{label}</option>)}
        </select>
      </label>
      <button className="btn btn-gold" disabled={busy}>{busy ? "Searching..." : "Search"}</button>
    </form>
  );
}