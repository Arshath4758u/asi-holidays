import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getRoom, voteRoom } from "../api";
import { rupees, useDocumentTitle } from "../hooks";
import WhatsAppButton from "../components/WhatsAppButton";

function store(key, make) {
  try {
    let v = localStorage.getItem(key);
    if (!v && make) { v = make(); localStorage.setItem(key, v); }
    return v || "";
  } catch { return make ? make() : ""; }
}
const newToken = () => (window.crypto?.randomUUID ? crypto.randomUUID() : `t${Date.now()}${Math.random().toString(36).slice(2)}`);

export default function Room() {
  const { code } = useParams();
  const [room, setRoom] = useState(null);
  const [missing, setMissing] = useState(false);
  const [name, setName] = useState(store("asi_voter_name"));
  const [token] = useState(() => store("asi_voter_token", newToken));
  const [msg, setMsg] = useState("");
  const link = `${window.location.origin}/room/${code}`;

  useDocumentTitle(room ? `${room.title} · Group trip room` : "Group trip room");

  const load = useCallback(() => getRoom(code).then(setRoom).catch((e) => e.status === 404 && setMissing(true)), [code]);
  useEffect(() => { load(); const t = setInterval(load, 10000); return () => clearInterval(t); }, [load]);

  const vote = async (optionId) => {
    if (!name.trim()) return setMsg("Enter your name first so everyone can see who voted.");
    setMsg("");
    try { localStorage.setItem("asi_voter_name", name.trim()); } catch { /* private mode */ }
    try { setRoom(await voteRoom(code, { option_id: optionId, voter_name: name.trim(), voter_token: token })); }
    catch { setMsg("Could not save your vote. Please try again."); }
  };

  const copy = async () => {
    try { await navigator.clipboard.writeText(link); setMsg("Link copied."); } catch { setMsg(link); }
  };

  if (missing) return <div className="wrap section"><p>This room does not exist.</p></div>;
  if (!room) return <div className="wrap section"><p>Loading...</p></div>;

  const totalVotes = room.options.reduce((n, o) => n + o.votes, 0);
  const leader = [...room.options].sort((a, b) => b.votes - a.votes)[0];

  return (
    <section className="section">
      <div className="wrap">
        <h1 className="h2">{room.title} · Group trip room</h1>
        <p className="lead-dark">Family and friends vote on options and see the cost per person.</p>
        <label className="share">Share this link
          <span className="share-row"><input readOnly value={link} onFocus={(e) => e.target.select()} /><button className="btn btn-gold" onClick={copy}>Copy link</button></span>
        </label>
        <label className="share">Your name
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="So others can see your vote" maxLength={40} />
        </label>
        {msg && <p className="fine" role="status">{msg}</p>}

        <div className="grid">
          {room.options.map((o) => (
            <article className="card" key={o.id}>
              {o.package.image ? <img src={o.package.image} alt={o.package.title} /> : <div className="ph">Photo coming soon</div>}
              <div className="card-body">
                <h3>{o.package.title}</h3>
                <p className="meta">₹{rupees(o.per_person)} per person · {o.votes} {o.votes === 1 ? "vote" : "votes"}</p>
                <div className="progress"><span style={{ width: `${totalVotes ? (o.votes / totalVotes) * 100 : 0}%` }} /></div>
                {o.voters.length > 0 && <p className="fine">{o.voters.join(", ")}</p>}
              </div>
              <button className="btn btn-gold btn-block" onClick={() => vote(o.id)}>Vote for this</button>
            </article>
          ))}
        </div>

        <h2 className="h3">Who is in</h2>
        <div className="chips">{room.people.length ? room.people.map((p) => <span className="chip on" key={p}>{p}</span>) : <span className="fine">No votes yet.</span>}</div>

        {leader && totalVotes > 0 && (
          <div className="side-card static">
            <h3>Total for {room.travellers} travellers</h3>
            <p>{leader.package.title}: ₹{rupees(leader.total)} · ₹{rupees(leader.per_person)} per person (indicative). Final quote confirmed by a consultant.</p>
            <WhatsAppButton variant="outline" label="Get a checked quote on WhatsApp" message={`Hi ASI Holidays, our group (${room.travellers} travellers) is leaning towards "${leader.package.title}". Room: ${link}`} />
          </div>
        )}
      </div>
    </section>
  );
}