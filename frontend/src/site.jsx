import { createContext, useContext, useEffect, useState } from "react";
import { getSite } from "./api";

const DEFAULTS = {
  whatsapp_number: import.meta.env.VITE_WHATSAPP_NUMBER || "",
  phone_display: "",
  email: "",
  address: "",
  opening_hours: "",
  response_time: "2 working hours",
  about_text: "ASI Holidays (ASI Global Travel) plans holidays and tours for individuals, families, groups and corporate clients.",
  mission: "Make holiday planning simple, personal and trustworthy for every traveller.",
};

const Ctx = createContext(DEFAULTS);
export const useSite = () => useContext(Ctx);

export function SiteProvider({ children }) {
  const [site, setSite] = useState(DEFAULTS);
  useEffect(() => {
    getSite()
      .then((d) => setSite({ ...DEFAULTS, ...Object.fromEntries(Object.entries(d).filter(([, v]) => v !== "")) }))
      .catch(() => {});
  }, []);
  return <Ctx.Provider value={site}>{children}</Ctx.Provider>;
}
