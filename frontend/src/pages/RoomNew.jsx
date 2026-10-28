import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createRoom, getPackages } from "../api";
import { rupees, useDocumentTitle } from "../hooks";

export default function RoomNew() {
  useDocumentTitle("Group trip room", "Share one link. Family and friends vote and see the cost per person.");
  const navigate = useNavigate();
  const [packages, setPackages] = useState([]);
  const [picked, setPicked] = useState([]);
  const [title, setTitle] = useState("");
  const [travellers, setTravellers] = useState(4);
  const [errors, setErrors] = useState({});

  useEffect(() => { getPackages().then(setPackages).catch(() => {}); }, []);

  const toggle = (slug) => setPicked(picked.includes(slug) ? picked.filter((s) => s !== slug) : picked.length < 5 ? [...picked, slug] : picked);

  const submit = async (e) => {
    e.preventDefault();
    setErrors({});
    try {
      const { code } = await createRoom({ title, travellers: Number(travellers), package_slugs: picked });
      navigate(`/room/${code}`);
    } catch (ex) {
      setErrors(ex.data || { title: ["Could not create the room."] });
    }
  };

  const err = (k) => errors[k] && <small className="err">{[].concat(errors[k]).join(" ")}</small>;

  return (
    <section className="section">
      <div className="wrap narrow">
        <h1 className="h2">Plan together</h1>
        <p className="lead-dark">Pick 2 to 5 packages. Share one link so family and friends can vote and see the cost per person.</p>
        <form className="form" onSubmit={submit}>
          <div className="row">
            <label>Trip name<input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Diwali holiday" maxLength={80} />{err("title")}</label>
            <label>Travellers<input type="number" min="1" max="50" value={travellers} onChange={(e) => setTravellers(e.target.value)} />{err("travellers")}</label>
          </div>
          <fieldset className="pick">
            <legend>Choose packages ({picked.length} of 5)</legend>
            {packages.map((p) => (
              <label key={p.slug} className="check">
                <input type="checkbox" checked={picked.includes(p.slug)} onChange={() => toggle(p.slug)} />
                <span>{p.title} · {p.duration_days} days · from ₹{rupees(p.price_from)}</span>
              </label>
            ))}
            {packages.length === 0 && <p>No packages yet.</p>}
          </fieldset>
          {err("package_slugs")}
          <button className="btn btn-gold">Create room</button>
        </form>
      </div>
    </section>
  );
}