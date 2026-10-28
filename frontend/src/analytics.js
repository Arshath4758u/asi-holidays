// Google Analytics 4. Does nothing unless VITE_GA_ID is set.
const ID = import.meta.env.VITE_GA_ID;

export function initAnalytics() {
  if (!ID) return;
  const s = document.createElement("script");
  s.async = true;
  s.src = `https://www.googletagmanager.com/gtag/js?id=${ID}`;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", ID, { send_page_view: false });
}

export function trackPageView(path) {
  if (window.gtag) window.gtag("event", "page_view", { page_path: path });
}

export function trackEvent(name, params = {}) {
  if (window.gtag) window.gtag("event", name, params);
}
