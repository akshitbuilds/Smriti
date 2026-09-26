import React, { useEffect, useState } from "react";
import { getCommitments } from "../api";
import CommitmentCard from "../components/CommitmentCard";

function getArray(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.data)) return data.data;
  if (Array.isArray(data?.items)) return data.items;
  return [];
}

export default function Commitments() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCommitments()
      .then((response) => {
        setItems(getArray(response.data));
      })
      .catch(() => {
        setError("Could not load commitments.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">TEAM MEMORY</p>
          <h1>Commitments</h1>
          <p className="subtitle">
            Tasks and promises extracted from team
            conversations.
          </p>
        </div>
      </div>

      {loading && (
        <div className="empty-card">
          Loading commitments...
        </div>
      )}

      {error && (
        <div className="error-box">{error}</div>
      )}

      {!loading && !error && items.length === 0 && (
        <div className="empty-card">
          No commitments returned by the backend.
        </div>
      )}

      <div className="cards-grid">
        {items.map((item, index) => (
          <CommitmentCard
            key={item.id || index}
            commitment={item}
          />
        ))}
      </div>
    </div>
  );
}