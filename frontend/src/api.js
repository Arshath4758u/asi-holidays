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


// Phase 2
export const planTrip = (query) => request("/ai/plan/", { method: "POST", body: JSON.stringify({ query }) });
export const getQuiz = () => request("/quiz/");
export const quizResult = (answers) => request("/quiz/result/", { method: "POST", body: JSON.stringify({ answers }) });
export const createRoom = (body) => request("/rooms/", { method: "POST", body: JSON.stringify(body) });
export const getRoom = (code) => request(`/rooms/${code}/`);
export const voteRoom = (code, body) => request(`/rooms/${code}/vote/`, { method: "POST", body: JSON.stringify(body) });
export const submitQuoteCheck = (body) => request("/ai/quote-check/", { method: "POST", body: JSON.stringify(body) });

// Phase 3
export const smartSearch = (body) => request("/search/", { method: "POST", body: JSON.stringify(body) });