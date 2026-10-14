const BASE = import.meta.env.VITE_API_URL || "/api";

async function request(path, options) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw Object.assign(new Error("Request failed"), { status: res.status, data });
  return data;
}

export const getPackages = (params = {}) => {
  const clean = Object.fromEntries(Object.entries(params).filter(([, v]) => v));
  const qs = new URLSearchParams(clean).toString();
  return request(`/packages/${qs ? `?${qs}` : ""}`);
};
export const getPackage = (slug) => request(`/packages/${slug}/`);
export const getSite = () => request("/site/");
export const getPolicies = () => request("/policies/");
export const submitEnquiry = (body) => request("/enquiries/", { method: "POST", body: JSON.stringify(body) });
export const trackWhatsAppClick = (body) =>
  request("/whatsapp-click/", { method: "POST", body: JSON.stringify(body) }).catch(() => {});