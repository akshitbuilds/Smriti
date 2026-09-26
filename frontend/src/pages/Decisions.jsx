import React, { useEffect, useState } from "react";
import { getDecisions } from "../api";
import DecisionCard from "../components/DecisionCard";

function getArray(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.data)) return data.data;
  if (Array.isArray(data?.items)) return data.items;
  return [];
}

export default function Decisions() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDecisions()
      .then((response) => {
        setItems(getArray(response.data));
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
          <h1>Decisions</h1>
          <p className="subtitle">
            See how team decisions changed over time.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="empty-card">
          Loading decisions...
        </div>
      ) : items.length === 0 ? (
        <div className="empty-card">
          No decisions returned by backend.
        </div>
      ) : (
        <div className="cards-grid">
          {items.map((item, index) => (
            <DecisionCard
              key={item.id || index}
              decision={item}
            />
          ))}
        </div>
      )}
    </div>
  );
}