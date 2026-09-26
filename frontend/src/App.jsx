import React, { useState } from "react";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import AskSmriti from "./pages/AskSmriti";
import Commitments from "./pages/Commitments";
import Decisions from "./pages/Decisions";
import Conflicts from "./pages/Conflicts";
import WeeklyBrief from "./pages/WeeklyBrief";
import Actions from "./pages/Actions";
import Audit from "./pages/Audit";

function App() {
  const [page, setPage] = useState("dashboard");

  function renderPage() {
    switch (page) {
      case "ask":
        return <AskSmriti />;

      case "commitments":
        return <Commitments />;

      case "decisions":
        return <Decisions />;

      case "conflicts":
        return <Conflicts />;

      case "weekly":
        return <WeeklyBrief />;

      case "actions":
        return <Actions />;

      case "audit":
        return <Audit />;

      case "dashboard":
      default:
        return <Dashboard />;
    }
  }

  return (
    <div className="app-shell">
      <Sidebar
        page={page}
        setPage={setPage}
      />

      <main className="main-content">
        <div className="top-status">
          <span className="local-dot"></span>
          LOCAL MODE
        </div>

        {renderPage()}
      </main>
    </div>
  );
}

export default App;