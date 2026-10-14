import { Link } from "react-router-dom";
import Brand from "./Brand";
import { useSite } from "../site";

export default function Footer() {
  const s = useSite();
  return (
    <footer className="footer">
      <div className="wrap footer-grid">
        <div>
          <Brand onDark />
          <p className="muted-light">asiholidays.in</p>
          <p><Link to="/about">About us</Link></p>
        </div>
        <div>
          <h4>Contact</h4>
          {s.phone_display && <p>{s.phone_display}</p>}
          {s.email && <p>{s.email}</p>}
          {s.address && <p>{s.address}</p>}
        </div>
        <div>
          <h4>Policies</h4>
          <p><Link to="/policies#privacy">Privacy policy</Link></p>
          <p><Link to="/policies#terms">Terms and conditions</Link></p>
          <p><Link to="/policies#cancellation">Cancellation and refunds</Link></p>
        </div>
      </div>
    </footer>
  );
}