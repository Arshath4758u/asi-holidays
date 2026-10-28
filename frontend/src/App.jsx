import { useEffect } from "react";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import WhatsAppButton from "./components/WhatsAppButton";
import { trackPageView } from "./analytics";
import Home from "./pages/Home";
import Packages from "./pages/Packages";
import PackageDetail from "./pages/PackageDetail";
import About from "./pages/About";
import Contact from "./pages/Contact";
import ThankYou from "./pages/ThankYou";
import Policies from "./pages/Policies";
import Planner from "./pages/Planner";
import Quiz from "./pages/Quiz";
import RoomNew from "./pages/RoomNew";
import Room from "./pages/Room";
import QuoteCheck from "./pages/QuoteCheck";
import Search from "./pages/Search";
function RouteEffects() {
  const { pathname, hash } = useLocation();
  useEffect(() => {
    if (!hash) window.scrollTo(0, 0);
    trackPageView(pathname);
  }, [pathname]);
  return null;
}

export default function App() {
  return (
    <>
      <RouteEffects />
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/packages" element={<Packages />} />
          <Route path="/packages/:slug" element={<PackageDetail />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/thank-you" element={<ThankYou />} />
          <Route path="/policies" element={<Policies />} />
          <Route path="/plan" element={<Planner />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/rooms/new" element={<RoomNew />} />
          <Route path="/room/:code" element={<Room />} />
          <Route path="/check-my-quote" element={<QuoteCheck />} />
          <Route path="/search" element={<Search />} />
          <Route path="*" element={<div className="wrap section"><p>Page not found. <Link className="link" to="/">Go home</Link></p></div>} />
        </Routes>
      </main>
      <Footer />
      <WhatsAppButton variant="floating" label="WhatsApp us" message="Hi ASI Holidays, I have a question." />
    </>
  );
}