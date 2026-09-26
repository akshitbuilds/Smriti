import React from "react";
import { CheckCircle2 } from "lucide-react";

export default function AuditRow({ item }) {
  const action =
    item.action ||
    item.description ||
    item.event ||
    "Action";

  const status =
    item.status ||
    "APPROVED";

  const timestamp =
    item.timestamp ||
    item.created_at ||
    item.date ||
    "";

  return (
    <div className="audit-row">
      <CheckCircle2 size={20} />

      <div className="audit-content">
        <strong>{action}</strong>

        <span>
          Status: {String(status).toUpperCase()}
        </span>

        {timestamp && (
          <small>{timestamp}</small>
        )}
      </div>
    </div>
  );
}