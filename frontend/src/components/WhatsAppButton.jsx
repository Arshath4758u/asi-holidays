import { trackWhatsAppClick } from "../api";
import { trackEvent } from "../analytics";
import { useSite } from "../site";

export function waUrl(number, message) {
  return `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
}

// variant: "gold" | "green" | "outline" | "floating"
export default function WhatsAppButton({ message, packageSlug = "", label = "WhatsApp us", variant = "gold", className = "" }) {
  const { whatsapp_number } = useSite();
  const onClick = () => {
    trackWhatsAppClick({ package_slug: packageSlug, page: window.location.pathname });
    trackEvent("whatsapp_click", { page: window.location.pathname, package: packageSlug });
  };
  return (
    <a
      className={`btn btn-${variant} ${className}`}
      href={waUrl(whatsapp_number, message)}
      target="_blank"
      rel="noopener noreferrer"
      onClick={onClick}
    >
      {label}
    </a>
  );
}
