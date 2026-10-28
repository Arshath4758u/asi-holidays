import { useEffect } from "react";

export function useDocumentTitle(title, description) {
  useEffect(() => {
    document.title = title ? `${title} | ASI Holidays` : "ASI Holidays | Holidays planned personally";
    if (description) {
      let m = document.querySelector('meta[name="description"]');
      if (!m) {
        m = document.createElement("meta");
        m.name = "description";
        document.head.appendChild(m);
      }
      m.content = description;
    }
  }, [title, description]);
}

export const rupees = (n) => Number(n).toLocaleString("en-IN");
