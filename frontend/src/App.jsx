import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Packages from "./pages/Packages";
import PackageDetail from "./pages/PackageDetail";
import EnquiryForm from "./components/EnquiryForm";
import WhatsAppButton from "./components/WhatsAppButton";

export default function App() {
  return (
    <>
      <header className="nav">
        <Link to="/" className="brand">ASI Holidays</Link>
        <nav>
          <Link to="/packages">Packages</Link>
          <Link to="/contact">Contact</Link>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/packages" element={<Packages />} />
          <Route path="/packages/:slug" element={<PackageDetail />} />
          <Route path="/contact" element={<section><h2>Plan your trip with us</h2><EnquiryForm /></section>} />
          <Route path="*" element={<p>Page not found.</p>} />
        </Routes>
      </main>
      <footer>
        <p>© ASI Holidays</p>
      </footer>
      <WhatsAppButton floating label="WhatsApp" message="Hi ASI Holidays, I have a question." />
    </>
  );
}
