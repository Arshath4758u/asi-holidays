import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getPolicies } from "../api";
import { useDocumentTitle } from "../hooks";

export default function Policies() {
  useDocumentTitle("Policies");
  const { hash } = useLocation();
  const [items, setItems] = useState([]);

  useEffect(() => { getPolicies().then(setItems).catch(() => {}); }, []);
  useEffect(() => {
    if (items.length && hash) document.getElementById(hash.slice(1))?.scrollIntoView({ behavior: "smooth" });
  }, [items, hash]);

  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">Policies</h1>
        <div className="layout-policies">
          <nav className="policy-nav">
            {items.map((p) => <a key={p.slug} href={`#${p.slug}`}>{p.title}</a>)}
          </nav>
          <div>
            {items.map((p) => (
              <article key={p.slug} id={p.slug} className="policy">
                <h2 className="h3">{p.title}</h2>
                <p className="pre">{p.body}</p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}