import React, { useEffect, useState } from "react";
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  GitBranch,
  ShieldCheck,
  RefreshCw,
} from "lucide-react";

import {
  getHealth,
  getCommitments,
  getDecisions,
  getConflicts,
} from "../api";

import StatCard from "../components/StatCard";
import CommitmentCard from "../components/CommitmentCard";
import DecisionCard from "../components/DecisionCard";
import ConflictCard from "../components/ConflictCard";

/*
  Converts different possible backend response formats
  into a simple array.

  Supported examples:

  [
    {...},
    {...}
  ]

  OR

  {
    "data": [...]
  }

  OR

  {
    "items": [...]
  }

  OR

  {
    "results": [...]
  }
*/
function getArray(data) {
  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data?.data)) {
    return data.data;
  }

  if (Array.isArray(data?.items)) {
    return data.items;
  }

  if (Array.isArray(data?.results)) {
    return data.results;
  }

  return [];
}

export default function Dashboard() {
  // -----------------------------
  // STATE
  // -----------------------------

  const [health, setHealth] = useState(null);

  const [commitments, setCommitments] = useState([]);

  const [decisions, setDecisions] = useState([]);

  const [conflicts, setConflicts] = useState([]);

  const [loading, setLoading] = useState(true);

  const [refreshing, setRefreshing] = useState(false);

  const [error, setError] = useState("");

  // -----------------------------
  // LOAD DASHBOARD DATA
  // -----------------------------

  async function loadDashboard(showRefresh = false) {
    try {
      setError("");

      if (showRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      /*
        Call all backend APIs.

        These correspond to:

        GET /health
        GET /commitments
        GET /decisions
        GET /conflicts
      */

      const [
        healthResponse,
        commitmentsResponse,
        decisionsResponse,
        conflictsResponse,
      ] = await Promise.allSettled([
        getHealth(),
        getCommitments(),
        getDecisions(),
        getConflicts(),
      ]);

      // -----------------------------
      // HEALTH
      // -----------------------------

      if (healthResponse.status === "fulfilled") {
        setHealth(healthResponse.value.data);
      } else {
        setHealth(null);
      }

      // -----------------------------
      // COMMITMENTS
      // -----------------------------

      if (commitmentsResponse.status === "fulfilled") {
        const data = commitmentsResponse.value.data;

        console.log("Commitments API:", data);

        setCommitments(getArray(data));
      } else {
        console.error(
          "Commitments API error:",
          commitmentsResponse.reason
        );

        setCommitments([]);
      }

      // -----------------------------
      // DECISIONS
      // -----------------------------

      if (decisionsResponse.status === "fulfilled") {
        const data = decisionsResponse.value.data;

        console.log("Decisions API:", data);

        setDecisions(getArray(data));
      } else {
        console.error(
          "Decisions API error:",
          decisionsResponse.reason
        );

        setDecisions([]);
      }

      // -----------------------------
      // CONFLICTS
      // -----------------------------

      if (conflictsResponse.status === "fulfilled") {
        const data = conflictsResponse.value.data;

        console.log("Conflicts API:", data);

        setConflicts(getArray(data));
      } else {
        console.error(
          "Conflicts API error:",
          conflictsResponse.reason
        );

        setConflicts([]);
      }

      /*
        If all APIs failed, show an error.
      */

      const allFailed =
        healthResponse.status === "rejected" &&
        commitmentsResponse.status === "rejected" &&
        decisionsResponse.status === "rejected" &&
        conflictsResponse.status === "rejected";

      if (allFailed) {
        setError(
          "Unable to connect to the Smriti backend. Make sure the backend is running on port 8000."
        );
      }
    } catch (err) {
      console.error("Dashboard error:", err);

      setError(
        "Something went wrong while loading dashboard data."
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  // -----------------------------
  // LOAD WHEN PAGE OPENS
  // -----------------------------

  useEffect(() => {
    loadDashboard();
  }, []);

  // -----------------------------
  // CALCULATE OVERDUE
  // -----------------------------

  const overdueCommitments = commitments.filter(
    (item) => {
      const status = String(
        item?.status || ""
      ).toUpperCase();

      return status === "OVERDUE";
    }
  );

  // -----------------------------
  // HEALTH STATUS
  // -----------------------------

  const healthOk =
    health?.status === "ok" ||
    health?.status === "healthy" ||
    health?.healthy === true ||
    health?.health === "ok";

  // -----------------------------
  // RENDER
  // -----------------------------

  return (
    <div className="page">

      {/* =====================================
          HEADER
      ====================================== */}

      <div className="page-header">

        <div>
          <p className="eyebrow">
            TEAM MEMORY OVERVIEW
          </p>

          <h1>
            Dashboard
          </h1>

          <p className="subtitle">
            Understand what your team decided,
            promised, changed and needs attention.
          </p>
        </div>

        <div
          className={`health-pill ${
            healthOk
              ? "healthy"
              : "unknown"
          }`}
        >
          <span></span>

          {healthOk
            ? "BACKEND CONNECTED"
            : "LOCAL MODE"}
        </div>

      </div>


      {/* =====================================
          ERROR MESSAGE
      ====================================== */}

      {error && (
        <div className="error-box">
          <strong>
            Backend connection problem
          </strong>

          <br />

          {error}

          <br />
          <br />

          <button
            className="secondary-button"
            onClick={() =>
              loadDashboard(true)
            }
          >
            <RefreshCw size={16} />

            Retry
          </button>
        </div>
      )}


      {/* =====================================
          STAT CARDS
      ====================================== */}

      <div className="stat-grid">

        <StatCard
          title="Commitments"
          value={commitments.length}
          icon={
            <CheckCircle2 size={22} />
          }
        />

        <StatCard
          title="Overdue"
          value={
            overdueCommitments.length
          }
          icon={
            <AlertTriangle size={22} />
          }
          type="danger"
        />

        <StatCard
          title="Decision Changes"
          value={decisions.length}
          icon={
            <GitBranch size={22} />
          }
          type="info"
        />

        <StatCard
          title="Conflicts"
          value={conflicts.length}
          icon={
            <ShieldCheck size={22} />
          }
          type="warning"
        />

      </div>


      {/* =====================================
          TEAM SITUATION
      ====================================== */}

      <div className="section-heading">

        <h2>
          Team situation
        </h2>

        <Activity size={20} />

      </div>


      {/* =====================================
          LOADING
      ====================================== */}

      {loading ? (

        <div className="empty-card">

          <RefreshCw
            size={22}
            style={{
              animation:
                "spin 1s linear infinite",
            }}
          />

          <p>
            Loading team memory...
          </p>

        </div>

      ) : (

        <div className="dashboard-grid">

          {/* =================================
              RECENT COMMITMENTS
          ================================== */}

          <section className="panel">

            <div className="panel-header">

              <h2>
                Recent commitments
              </h2>

              <span className="status-badge">
                {commitments.length}
              </span>

            </div>


            {commitments.length === 0 ? (

              <div className="empty-state">

                <CheckCircle2
                  size={25}
                />

                <p>
                  No commitments returned
                  by backend.
                </p>

              </div>

            ) : (

              commitments
                .slice(0, 5)
                .map((item, index) => (

                  <CommitmentCard
                    key={
                      item?.id ||
                      item?.commitment_id ||
                      index
                    }
                    commitment={item}
                  />

                ))

            )}

          </section>


          {/* =================================
              RECENT DECISIONS
          ================================== */}

          <section className="panel">

            <div className="panel-header">

              <h2>
                Recent decisions
              </h2>

              <span className="status-badge changed">
                {decisions.length}
              </span>

            </div>


            {decisions.length === 0 ? (

              <div className="empty-state">

                <GitBranch
                  size={25}
                />

                <p>
                  No decisions returned
                  by backend.
                </p>

              </div>

            ) : (

              decisions
                .slice(0, 5)
                .map((item, index) => (

                  <DecisionCard
                    key={
                      item?.id ||
                      item?.decision_id ||
                      index
                    }
                    decision={item}
                  />

                ))

            )}

          </section>

        </div>

      )}


      {/* =====================================
          CONFLICTS
      ====================================== */}

      {conflicts.length > 0 && (

        <section
          className="panel"
          style={{
            marginTop: "20px",
          }}
        >

          <div className="panel-header">

            <h2>
              Conflicts requiring attention
            </h2>

            <span className="status-badge conflict">
              {conflicts.length}
            </span>

          </div>


          {conflicts
            .slice(0, 5)
            .map((item, index) => (

              <ConflictCard
                key={
                  item?.id ||
                  item?.conflict_id ||
                  index
                }
                conflict={item}
              />

            ))}

        </section>

      )}


      {/* =====================================
          SOVEREIGNTY PANEL
      ====================================== */}

      <section className="sovereignty-panel">

        <div className="sovereignty-icon">

          <ShieldCheck />

        </div>


        <div>

          <h2>
            WHY SMRITI IS SOVEREIGN
          </h2>


          <div className="sovereignty-items">

            <span>
              ✓ Runs locally
            </span>

            <span>
              ✓ Team data stays on the machine
            </span>

            <span>
              ✓ Evidence-backed answers
            </span>

            <span>
              ✓ Human approval required
            </span>

            <span>
              ✓ Actions are audited
            </span>

          </div>

        </div>

      </section>


      {/* =====================================
          DATA FLOW
      ====================================== */}

      <section className="flow-panel">

        <h2>
          How it works
        </h2>


        <div className="flow">

          <div>
            WhatsApp Export
          </div>

          <span>↓</span>

          <div>
            Parser
          </div>

          <span>↓</span>

          <div>
            Team Memory
          </div>

          <span>↓</span>

          <div>
            Evidence + Retrieval
          </div>

          <span>↓</span>

          <div>
            Smriti AI
          </div>

          <span>↓</span>


          <div className="flow-split">

            <div>

              <strong>
                Answer
              </strong>

              <small>
                ↓
              </small>

              <span>
                Evidence
              </span>

            </div>


            <div>

              <strong>
                Action
              </strong>

              <small>
                ↓
              </small>

              <span>
                Approval → Audit
              </span>

            </div>

          </div>

        </div>

      </section>


      {/* =====================================
          REFRESH
      ====================================== */}

      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          marginTop: "18px",
        }}
      >

        <button
          className="secondary-button"
          onClick={() =>
            loadDashboard(true)
          }
          disabled={refreshing}
        >

          <RefreshCw
            size={16}
            style={
              refreshing
                ? {
                    animation:
                      "spin 1s linear infinite",
                  }
                : {}
            }
          />

          {refreshing
            ? "Refreshing..."
            : "Refresh dashboard"}

        </button>

      </div>

    </div>
  );
}