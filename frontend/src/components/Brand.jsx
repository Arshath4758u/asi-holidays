import { useState } from "react";
import { Link } from "react-router-dom";

// Put the client's logo at frontend/public/logo.png. Falls back to text if it is missing.
export default function Brand({ onDark = false }) {
  const [hasLogo, setHasLogo] = useState(true);
  return (
    <Link to="/" className={onDark ? "brand brand-box" : "brand"} aria-label="ASI Holidays home">
      {hasLogo ? <img src="/logo.png" alt="ASI Holidays" onError={() => setHasLogo(false)} /> : <span>ASI Holidays</span>}
    </Link>
  );
}