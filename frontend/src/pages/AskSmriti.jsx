import React, { useState } from "react";
import { Send, MessageCircleQuestion } from "lucide-react";
import { askSmriti } from "../api";
import EvidenceCard from "../components/EvidenceCard";

export default function AskSmriti() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk(e) {
    e.preventDefault();

    if (!question.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await askSmriti(question);

      const data = response.data;

      setAnswer(
        data.answer ||
        data.response ||
        data.message ||
        "No answer returned."
      );

      const evidenceData =
        data.evidence ||
        data.sources ||
        data.messages ||
        [];

      setEvidence(
        Array.isArray(evidenceData)
          ? evidenceData
          : [evidenceData]
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to contact the Smriti backend."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">TEAM MEMORY</p>
          <h1>Ask Smriti</h1>
          <p className="subtitle">
            Ask questions and trace the answer back to
            evidence.
          </p>
        </div>

        <MessageCircleQuestion size={36} />
      </div>

      <form
        className="ask-box"
        onSubmit={handleAsk}
      >
        <textarea
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Why did we change the venue?"
          rows={5}
        />

        <button
          className="primary-button ask-button"
          disabled={loading}
        >
          <Send size={17} />

          {loading
            ? "Thinking..."
            : "Ask Smriti"}
        </button>
      </form>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {answer && (
        <section className="answer-panel">
          <p className="eyebrow">ANSWER</p>

          <h2>{answer}</h2>
        </section>
      )}

      {evidence.length > 0 && (
        <section className="panel">
          <div className="panel-header">
            <h2>Evidence</h2>
          </div>

          <div className="evidence-list">
            {evidence.map((item, index) => (
              <EvidenceCard
                key={index}
                evidence={item}
              />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}