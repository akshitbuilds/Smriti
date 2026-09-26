import React from "react";
import { AlertTriangle } from "lucide-react";

export default function ConflictCard({ conflict }) {
  const title =
    conflict.title ||
    conflict.task ||
    conflict.subject ||
    "Conflict detected";

  const status =
    conflict.status ||
    "CONFLICT";

  const items =
    conflict.items ||
    conflict.evidence ||
    conflict.messages ||
    [];

  return (
    <div className="conflict-card">
      <div className="conflict-title">
        <AlertTriangle size={20} />
        <strong>CONFLICT DETECTED</strong>
      </div>

      <h3>{title}</h3>

      {Array.isArray(items) &&
        items.map((item, index) => (
          <div className="conflict-item" key={index}>
            {typeof item === "string"
              ? item
              : item.text || item.message || ""}
          </div>
        ))}

      <span className="status-badge conflict">
        {String(status).toUpperCase()}
      </span>
    </div>
  );
}