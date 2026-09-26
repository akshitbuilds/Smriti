import React, { useEffect, useState } from "react";
import {
  getPendingActions,
  approveAction,
} from "../api";

import ActionCard from "../components/ActionCard";

function getArray(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.data)) return data.data;
  if (Array.isArray(data?.items)) return data.items;
  return [];
}

export default function Actions() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [approving, setApproving] = useState(null);
  const [error, setError] = useState("");

  async function loadActions() {
    try {
      const response = await getPendingActions();
      setItems(getArray(response.data));
    } catch {
      setError("Could not load pending actions.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadActions();
  }, []);

  async function handleApprove(id) {
    if (!id) {
      setError("Action ID was not returned by backend.");
      return;
    }

    try {
      setApproving(id);

      await approveAction(id);

      // Refresh pending actions immediately
      await loadActions();
    } catch {
      setError("Could not approve the action.");
    } finally {
      setApproving(null);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">
            HUMAN APPROVAL
          </p>

          <h1>Approval Inbox</h1>

          <p className="subtitle">
            Smriti suggests. A human approves.
          </p>
        </div>
      </div>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {loading ? (
        <div className="empty-card">
          Loading pending actions...
        </div>
      ) : items.length === 0 ? (
        <div className="empty-card">
          No actions currently require approval.
        </div>
      ) : (
        <div className="cards-grid">
          {items.map((item, index) => {
            const id = item.id || item.action_id;

            return (
              <ActionCard
                key={id || index}
                action={item}
                onApprove={handleApprove}
                approving={approving === id}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}