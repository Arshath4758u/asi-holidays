import { trackWhatsAppClick } from "../api";

const NUMBER = import.meta.env.VITE_WHATSAPP_NUMBER || "919999999999";

export default function WhatsAppButton({ message, packageSlug, label = "Enquire on WhatsApp", floating = false }) {
  const href = `https://wa.me/${NUMBER}?text=${encodeURIComponent(message)}`;
  const onClick = () => trackWhatsAppClick({ package_slug: packageSlug || "", page: window.location.pathname });
  return (
    <a
      className={floating ? "wa-btn wa-floating" : "wa-btn"}
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      onClick={onClick}
    >
      {label}
    </a>
  );
}
