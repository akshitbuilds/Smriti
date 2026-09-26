import React from "react";
import { Clock3, CheckCircle2 } from "lucide-react";

export default function CommitmentCard({ commitment }) {
  const person =
    commitment.person ||
    commitment.assignee ||
    commitment.owner ||
    commitment.name ||
    "Unknown";

  const task =
    commitment.task ||
    commitment.title ||
    commitment.description ||
    "Unnamed commitment";

  const deadline =
    commitment.deadline ||
    commitment.due_date ||
    commitment.due ||
    "No deadline";

  const status =
    commitment.status ||
    "PENDING";

  const evidence =
    commitment.evidence ||
    commitment.message ||
    commitment.quote ||
    "";

  const normalized = String(status).toUpperCase();

  return (
    <div className="commitment-card">
      <div className="card-top">
        <span
          className={`status-badge ${
            normalized === "COMPLETED"
              ? "completed"
              : normalized === "OVERDUE"
              ? "overdue"
              : "pending"
          }`}
        >
          {normalized}
        </span>
      </div>

      <h3>{task}</h3>

      <p className="muted">
        <strong>{person}</strong>
      </p>

      <div className="detail-row">
        <Clock3 size={16} />
        <span>Deadline: {deadline}</span>
      </div>

      {evidence && (
        <div className="mini-evidence">
          "{evidence}"
        </div>
      )}

      {normalized === "COMPLETED" && (
        <CheckCircle2 size={18} />
      )}
    </div>
  );
}