import React from "react";
import { GitBranch } from "lucide-react";

export default function DecisionCard({ decision }) {
  const statement =
    decision.statement ||
    decision.title ||
    decision.description ||
    "Unnamed decision";

  const person =
    decision.person ||
    decision.owner ||
    "Unknown";

  const evidence =
    decision.evidence ||
    decision.source_quote ||
    decision.quote ||
    "";

  return (
    <div className="commitment-card">
      <div className="card-top">
        <span className="status-badge changed">
          DECISION
        </span>
      </div>

      <h3>{statement}</h3>

      <p className="muted">
        <strong>{person}</strong>
      </p>

      {evidence && (
        <div className="mini-evidence">
          "{evidence}"
        </div>
      )}

      <GitBranch size={16} />
    </div>
  );
}
