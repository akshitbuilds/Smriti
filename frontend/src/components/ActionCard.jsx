import React from "react";
import { Check, Eye } from "lucide-react";

export default function ActionCard({
  action,
  onApprove,
  approving,
}) {
  const id = action.id || action.action_id;

  const title =
    action.title ||
    action.action ||
    action.description ||
    "Action requires approval";

  const evidence =
    action.evidence ||
    action.messages ||
    [];

  const evidenceList = Array.isArray(evidence)
    ? evidence
    : [evidence];

  return (
    <div className="action-card">
      <span className="status-badge approval">
        ACTION REQUIRES APPROVAL
      </span>

      <h3>{title}</h3>

      <h4>Evidence</h4>

      {evidenceList.map((item, index) => (
        <p key={index}>
          {typeof item === "string"
            ? item
            : item.text ||
              item.message ||
              `Message ${index + 1}`}
        </p>
      ))}

      <div className="action-buttons">
        <button
          className="primary-button"
          onClick={() => onApprove(id)}
          disabled={approving}
        >
          <Check size={16} />
          {approving ? "Approving..." : "Approve"}
        </button>

        <button className="secondary-button">
          <Eye size={16} />
          Review
        </button>
      </div>
    </div>
  );
}