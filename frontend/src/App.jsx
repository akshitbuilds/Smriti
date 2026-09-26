import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askSmriti = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setEvidence([]);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();

      setAnswer(data.answer || "No answer returned.");
      setEvidence(data.evidence || []);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to reach Smriti backend. Make sure FastAPI and ngrok are running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Smriti</h1>
        <p>Sovereign Team Memory</p>
      </header>

      <section className="stats">
        <div className="card">
          <h2>23</h2>
          <p>Memories</p>
        </div>

        <div className="card">
          <h2>5</h2>
          <p>Commitments</p>
        </div>

        <div className="card">
          <h2>2</h2>
          <p>Conflicts</p>
        </div>

        <div className="card">
          <h2>1</h2>
          <p>Overdue</p>
        </div>
      </section>

      <section className="ask">
        <h2>Ask Smriti</h2>

        <div className="ask-row">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askSmriti();
              }
            }}
            placeholder="Ask about a decision, commitment or deadline..."
          />

          <button onClick={askSmriti} disabled={loading}>
            {loading ? "Thinking..." : "Ask Smriti"}
          </button>
        </div>

        {error && <p className="error">{error}</p>}

        {answer && (
          <div className="answer">
            <h3>Smriti's Answer</h3>
            <p>{answer}</p>
          </div>
        )}

        {evidence.length > 0 && (
          <div className="evidence">
            <h3>Evidence</h3>

            {evidence.map((item, index) => (
              <div className="evidence-item" key={index}>
                <strong>
                  {item.sender} · {item.timestamp}
                </strong>

                <p>"{item.quote}"</p>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="content">
        <div className="panel">
          <h2>Recent Commitments</h2>

          <p>
            <strong>Rohan</strong> — Poster
          </p>

          <p>
            <strong>Akash</strong> — Sponsorship deck
          </p>
        </div>

        <div className="panel">
          <h2>Recent Decisions</h2>

          <p>Venue changed to Hall B</p>

          <p>Auditorium unavailable on August 28</p>
        </div>
      </section>
    </div>
  );
}

export default App;