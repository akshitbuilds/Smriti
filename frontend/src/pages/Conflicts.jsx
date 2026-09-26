import React, { useEffect, useState } from "react";
import { getConflicts } from "../api";
import ConflictCard from "../components/ConflictCard";

function getArray(data) {
  if (Array.isArray(data)) return data;

  if (Array.isArray(data?.data)) {
    return data.data;
  }

  if (Array.isArray(data?.items)) {
    return data.items;
  }

  if (Array.isArray(data?.conflicts)) {
    return data.conflicts;
  }

  return [];
}

export default function Conflicts() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadConflicts() {
    try {
      setLoading(true);
      setError("");

      const response = await getConflicts();

      setItems(getArray(response));
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to the backend. Conflicts could not be loaded."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadConflicts();
  }, []);

  return (
    <div className="page">

      <div className="page-header">
        <div>
          <p className="eyebrow">TEAM MEMORY</p>

          <h1>Conflicts</h1>

          <p className="subtitle">
            Detect conflicting commitments, decisions, or messages.
          </p>
        </div>
      </div>

      {loading && (
        <div className="empty-card">
          Loading conflicts...
        </div>
      )}

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {!loading && !error && items.length === 0 && (
        <div className="empty-card">
          No conflicts returned by the backend.
        </div>
      )}

      {!loading && !error && items.length > 0 && (
        <div className="cards-grid">
          {items.map((item, index) => (
            <ConflictCard
              key={item.id || item.conflict_id || index}
              conflict={item}
            />
          ))}
        </div>
      )}

    </div>
  );
}