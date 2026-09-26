// Local dev talks to your own machine by default. Only set
// VITE_API_BASE (in a .env file next to package.json) if you're
// exposing the backend through ngrok or similar, e.g.:
//   VITE_API_BASE=https://your-id.ngrok-free.dev
const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function request(path, options = {}) {
  const separator = path.includes("?") ? "&" : "?";

  const url =
    `${API_BASE}${path}${separator}ngrok-skip-browser-warning=true`;

  const headers = {
    ...(options.body
      ? { "Content-Type": "application/json" }
      : {}),
    ...(options.headers || {}),
  };

  console.log("SMRITI API REQUEST:", url);

  const response = await fetch(url, {
    ...options,
    headers,
  });

  console.log(
    "SMRITI API RESPONSE:",
    response.status,
    response.statusText
  );

  if (!response.ok) {
    throw new Error(
      `Backend error: ${response.status} ${response.statusText}`
    );
  }

  const data = await response.json();

  // Pages in this app read `response.data`, so wrap the parsed JSON
  // the same way an axios client would.
  return { data };
}


// ============================================================
// MAIN API
// ============================================================

export const api = {

  health: () =>
    request("/health"),

  messages: () =>
    request("/messages"),

  memories: () =>
    request("/memories"),

  commitments: () =>
    request("/commitments"),

  decisions: () =>
    request("/decisions"),

  conflicts: () =>
    request("/conflicts"),

  weeklyBrief: () =>
    request("/weekly-brief"),

  ask: (question) =>
    request("/ask", {
      method: "POST",
      body: JSON.stringify({
        question,
      }),
    }),

  pendingActions: () =>
    request("/actions/pending"),

  proposeAction: (
    type,
    description,
    evidence = []
  ) =>
    request("/actions/propose", {
      method: "POST",
      body: JSON.stringify({
        type,
        description,
        evidence,
      }),
    }),

  approveAction: (actionId) =>
    request(`/actions/${actionId}/approve`, {
      method: "POST",
    }),

  audit: () =>
    request("/audit"),
};


// ============================================================
// COMPATIBILITY FUNCTIONS
// ============================================================

export const getHealth = () =>
  api.health();

export const getMessages = () =>
  api.messages();

export const getMemories = () =>
  api.memories();

export const getCommitments = () =>
  api.commitments();

export const getDecisions = () =>
  api.decisions();

export const getConflicts = () =>
  api.conflicts();

export const getWeeklyBrief = () =>
  api.weeklyBrief();

export const askSmriti = (question) =>
  api.ask(question);

export const getPendingActions = () =>
  api.pendingActions();

export const proposeAction = (
  type,
  description,
  evidence = []
) =>
  api.proposeAction(
    type,
    description,
    evidence
  );

export const approveAction = (actionId) =>
  api.approveAction(actionId);

export const getAudit = () =>
  api.audit();

export default api;
