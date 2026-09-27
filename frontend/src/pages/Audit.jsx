import React, { useEffect, useState } from "react";
import { getAudit } from "../api";
import AuditRow from "../components/AuditRow";

function getArray(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.data)) return data.data;
  if (Array.isArray(data?.items)) return data.items;
  return [];
}

export default function Audit() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAudit()
      .then((response) => {
        setItems(getArray(response));
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">
            TRACEABILITY
          </p>

          <h1>Audit Log</h1>

          <p className="subtitle">
            Every approved action leaves a visible record.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="empty-card">
          Loading audit log...
        </div>
      ) : items.length === 0 ? (
        <div className="empty-card">
          No audit records returned by backend.
        </div>
      ) : (
        <div className="audit-list">
          {items.map((item, index) => (
            <AuditRow
              key={item.id || index}
              item={item}
            />
          ))}
        </div>
      )}
    </div>
  );
}