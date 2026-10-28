import { useEffect, useState } from "react";
import { getQuiz, quizResult } from "../api";
import { useDocumentTitle } from "../hooks";
import PackageCard from "../components/PackageCard";

export default function Quiz() {
  useDocumentTitle("Travel mood quiz", "Five questions. Get a shareable travel mood card and matching packages.");
  const [questions, setQuestions] = useState(null);
  const [i, setI] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => { getQuiz().then((d) => setQuestions(d.questions)).catch(() => setError(true)); }, []);

  if (error) return <div className="wrap section"><p>The quiz could not load. Please try again.</p></div>;
  if (!questions) return <div className="wrap section"><p>Loading...</p></div>;

  const q = questions[i];
  const last = i === questions.length - 1;
  const choose = (key) => setAnswers([...answers.slice(0, i), key]);

  const next = async () => {
    if (!last) return setI(i + 1);
    try { setResult(await quizResult(answers)); } catch { setError(true); }
  };

  const share = async () => {
    const text = `I am ${result.mood.title}! ${result.mood.line} Find your travel mood with ASI Holidays:`;
    const url = `${window.location.origin}/quiz`;
    if (navigator.share) { try { await navigator.share({ title: result.mood.title, text, url }); return; } catch { /* cancelled */ } }
    window.open(`https://wa.me/?text=${encodeURIComponent(`${text} ${url}`)}`, "_blank", "noopener");
  };

  const restart = () => { setResult(null); setAnswers([]); setI(0); };

  if (result) {
    return (
      <section className="section">
        <div className="wrap narrow">
          <div className="result-card">
            <p className="eyebrow">Your travel mood</p>
            <h1>You are {result.mood.title}</h1>
            <p>{result.mood.line}</p>
            <button className="btn btn-gold" onClick={share}>Share result</button>
            <button className="link-btn light" onClick={restart}>Take the quiz again</button>
          </div>
          <h2 className="h3">Packages that match your style</h2>
          <div className="grid">{result.packages.map((p) => <PackageCard key={p.slug} pkg={p} />)}</div>
        </div>
      </section>
    );
  }

  return (
    <section className="section">
      <div className="wrap narrow">
        <h1 className="h2">Travel mood quiz</h1>
        <p className="lead-dark">Five questions. A result card you can share, plus matching packages.</p>
        <div className="side-card static">
          <p className="step-label">Question {i + 1} of {questions.length}</p>
          <div className="progress" role="progressbar" aria-valuemin="0" aria-valuemax={questions.length} aria-valuenow={i + 1}><span style={{ width: `${((i + 1) / questions.length) * 100}%` }} /></div>
          <h2 className="h3">{q.text}</h2>
          <div className="options">
            {q.options.map((o) => (
              <button key={o.key} type="button" className={answers[i] === o.key ? "option on" : "option"} onClick={() => choose(o.key)}>{o.label}</button>
            ))}
          </div>
          <div className="nav-row">
            <button className="btn btn-outline" disabled={i === 0} onClick={() => setI(i - 1)}>Back</button>
            <button className="btn btn-gold" disabled={!answers[i]} onClick={next}>{last ? "See my result" : "Next"}</button>
          </div>
        </div>
      </div>
    </section>
  );
}