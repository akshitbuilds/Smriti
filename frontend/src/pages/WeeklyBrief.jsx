import React, { useEffect, useState } from "react";
import {
  getWeeklyBrief,
} from "../api";

export default function WeeklyBrief() {
  const [brief, setBrief] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getWeeklyBrief()
      .then((response) => {
        setBrief(response.data);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="page">
        <div className="empty-card">
          Loading weekly brief...
        </div>
      </div>
    );
  }

  if (!brief) {
    return (
      <div className="page">
        <div className="empty-card">
          No weekly brief returned by backend.
        </div>
      </div>
    );
  }

  const commitments =
    brief.commitments ??
    brief.total_commitments ??
    0;

  const overdue =
    brief.overdue ??
    brief.total_overdue ??
    0;

  const changes =
    brief.changes ??
    brief.decision_changes ??
    0;

  const conflicts =
    brief.conflicts ??
    brief.total_conflicts ??
    0;

  const attention =
    brief.needs_attention ||
    brief.attention ||
    [];

  const decisionChanges =
    brief.decision_changes_list ||
    brief.decisions ||
    [];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">
            EXECUTIVE SUMMARY
          </p>
          <h1>This Week's Team Brief</h1>
        </div>
      </div>

      <div className="brief-stats">
        <div>
          <strong>{commitments}</strong>
          <span>Commitments</span>
        </div>

        <div>
          <strong>{overdue}</strong>
          <span>Overdue</span>
        </div>

        <div>
          <strong>{changes}</strong>
          <span>Changes</span>
        </div>

        <div>
          <strong>{conflicts}</strong>
          <span>Conflicts</span>
        </div>
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <h2>Needs Attention</h2>

          {attention.length === 0 ? (
            <p className="muted">
              No attention items returned.
            </p>
          ) : (
            <ul className="clean-list">
              {attention.map((item, index) => (
                <li key={index}>
                  {typeof item === "string"
                    ? item
                    : item.text ||
                      item.task ||
                      item.description ||
                      ""}
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="panel">
          <h2>Decision Changes</h2>

          {decisionChanges.length === 0 ? (
            <p className="muted">
              No decision changes returned.
            </p>
          ) : (
            <ul className="clean-list">
              {decisionChanges.map((item, index) => (
                <li key={index}>
                  {typeof item === "string"
                    ? item
                    : item.text ||
                      item.description ||
                      item.updated ||
                      ""}
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}