import React from "react";
import { GitBranch } from "lucide-react";

export default function DecisionCard({ decision }) {
  const topic = decision?.topic || "Decision";
  const from = decision?.from || "Unknown";
  const to = decision?.to || "Unknown";
  const reason = decision?.reason || "";
  const evidence = decision?.evidence || [];

  return (
    <div className="commitment-card">
      <div className="card-top">
        <span className="status-badge changed">
          CHANGED
        </span>
      </div>

      <h3>{topic}</h3>

      <p className="muted">
        <strong>{from}</strong> → <strong>{to}</strong>
      </p>

      {reason && (
        <div className="detail-row">
          <GitBranch size={16} />
          <span>{reason}</span>
        </div>
      )}

      {evidence.length > 0 && (
        <div className="mini-evidence">
          "{evidence[0].quote}"
        </div>
      )}
    </div>
  );
}