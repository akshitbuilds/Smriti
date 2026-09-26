import React from "react";

export default function StatCard({ title, value, icon, type = "normal" }) {
  return (
    <div className={`stat-card ${type}`}>
      <div className="stat-icon">{icon}</div>

      <div>
        <div className="stat-value">{value ?? 0}</div>
        <div className="stat-title">{title}</div>
      </div>
    </div>
  );
}