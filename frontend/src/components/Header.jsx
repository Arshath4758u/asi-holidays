import { useState } from "react";
import { Link } from "react-router-dom";
import Brand from "./Brand";
import WhatsAppButton from "./WhatsAppButton";

const LINKS = [
  ["India holidays", "/packages?region=india"],
  ["International", "/packages?region=international"],
  ["Honeymoon", "/packages?category=honeymoon"],
  ["Group tours", "/packages?category=group"],
  ["Contact", "/contact"],
];

export default function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="header">
      <div className="wrap header-row">
        <Brand />
        <nav className={open ? "nav open" : "nav"} aria-label="Main">
          {LINKS.map(([label, to]) => (
            <Link key={label} to={to} onClick={() => setOpen(false)}>{label}</Link>
          ))}
        </nav>
        <WhatsAppButton className="header-wa" message="Hi ASI Holidays, I'd like help planning a holiday." />
        <button className="burger" aria-label="Menu" aria-expanded={open} onClick={() => setOpen(!open)}>≡</button>
      </div>
    </header>
  );
}