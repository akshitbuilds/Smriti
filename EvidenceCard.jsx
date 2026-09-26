import React from "react";

export default function EvidenceCard({ evidence }) {
  const text =
    typeof evidence === "string"
      ? evidence
      : evidence?.text ||
        evidence?.message ||
        evidence?.quote ||
        "";

  const sender =
    typeof evidence === "object"
      ? evidence?.sender || evidence?.person
      : null;

  const timestamp =
    typeof evidence === "object"
      ? evidence?.timestamp
      : null;

  return (
    <div className="mini-evidence">
      "{text}"
      {(sender || timestamp) && (
        <div className="muted" style={{ marginTop: 6, fontSize: 12 }}>
          {sender}
          {sender && timestamp ? " · " : ""}
          {timestamp}
        </div>
      )}
    </div>
  );
}
