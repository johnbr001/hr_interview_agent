import { useState } from "react";
import {
  createSession,
  listTurns,
  scoreTurn,
  uploadRagPdf,
  type ScoreTurn,
  type Session,
} from "./api";

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [interviewer, setInterviewer] = useState("");
  const [candidate, setCandidate] = useState("");
  const [role, setRole] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [useWeb, setUseWeb] = useState(false);
  const [latest, setLatest] = useState<ScoreTurn | null>(null);
  const [history, setHistory] = useState<ScoreTurn[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function startSession() {
    setError(null);
    setLoading(true);
    try {
      const s = await createSession({
        interviewerName: interviewer,
        candidateName: candidate,
        roleTitle: role || undefined,
      });
      setSession(s);
      setHistory([]);
      setLatest(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create session");
    } finally {
      setLoading(false);
    }
  }

  async function submitScore() {
    if (!session) return;
    setError(null);
    setLoading(true);
    try {
      const turn = await scoreTurn(session.id, {
        intervieweeText: answer,
        questionContext: question || undefined,
        useWebSearch: useWeb,
      });
      setLatest(turn);
      setAnswer("");
      const turns = await listTurns(session.id);
      setHistory(turns);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Scoring failed");
    } finally {
      setLoading(false);
    }
  }

  async function onPdfUpload(file: File | null) {
    if (!file) return;
    setError(null);
    setLoading(true);
    try {
      await uploadRagPdf(file);
      alert("PDF ingested into RAG index.");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>HR Interview Scorer</h1>
        <p>
          Type what the interviewee says. The AI agent scores each answer (A–F)
          using your PDF Q&amp;A guides and optional web search.
        </p>
      </header>

      {error && <p className="error">{error}</p>}

      {!session ? (
        <section className="card">
          <h2>Start interview</h2>
          <div className="row">
            <div>
              <label>Interviewer name</label>
              <input
                value={interviewer}
                onChange={(e) => setInterviewer(e.target.value)}
                placeholder="Your name"
              />
            </div>
            <div>
              <label>Candidate name</label>
              <input
                value={candidate}
                onChange={(e) => setCandidate(e.target.value)}
                placeholder="Interviewee"
              />
            </div>
          </div>
          <label>Role / position (optional)</label>
          <input
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="e.g. Software Engineer L3"
          />
          <button
            type="button"
            disabled={loading || !interviewer || !candidate}
            onClick={startSession}
          >
            Begin session
          </button>
        </section>
      ) : (
        <>
          <section className="card">
            <h2>
              Session: {session.candidateName}
              {session.roleTitle ? ` — ${session.roleTitle}` : ""}
            </h2>
            <p style={{ margin: 0, color: "#666", fontSize: "0.9rem" }}>
              Interviewer: {session.interviewerName}
            </p>
          </section>

          <section className="card">
            <h2>Upload Q&amp;A PDF (RAG)</h2>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => onPdfUpload(e.target.files?.[0] ?? null)}
            />
          </section>

          <section className="card">
            <h2>Score answer</h2>
            <label>Question or topic (optional)</label>
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. Tell me about a conflict you resolved"
            />
            <label>What the interviewee said</label>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type or paste the candidate's response..."
            />
            <label className="checkbox">
              <input
                type="checkbox"
                checked={useWeb}
                onChange={(e) => setUseWeb(e.target.checked)}
              />
              Use internet search (MCP) for supplementary context
            </label>
            <button
              type="button"
              disabled={loading || !answer.trim()}
              onClick={submitScore}
            >
              Get score
            </button>
          </section>

          {latest && (
            <section className="card">
              <h2>Latest score</h2>
              <div className={`grade grade-${latest.grade}`}>{latest.grade}</div>
              <p>{latest.rationale}</p>
            </section>
          )}

          {history.length > 0 && (
            <section className="card">
              <h2>History</h2>
              {[...history].reverse().map((t) => (
                <div key={t.id} className="history-item">
                  <strong className={`grade-${t.grade}`}>Grade {t.grade}</strong>
                  {t.questionContext && (
                    <p>
                      <em>Q:</em> {t.questionContext}
                    </p>
                  )}
                  <p>
                    <em>Said:</em> {t.intervieweeText}
                  </p>
                  <p>{t.rationale}</p>
                </div>
              ))}
            </section>
          )}

          <button
            type="button"
            className="secondary"
            onClick={() => {
              setSession(null);
              setLatest(null);
              setHistory([]);
            }}
          >
            End session
          </button>
        </>
      )}
    </div>
  );
}
