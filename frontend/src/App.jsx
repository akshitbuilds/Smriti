import { Routes, Route } from "react-router-dom";

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
  return (
    <div className="app-shell">
      <Sidebar />

      <main className="main-content">
        <div className="top-status">
          <span className="local-dot"></span>
          LOCAL MODE
        </div>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/ask" element={<AskSmriti />} />
          <Route path="/commitments" element={<Commitments />} />
          <Route path="/decisions" element={<Decisions />} />
          <Route path="/conflicts" element={<Conflicts />} />
          <Route path="/weekly-brief" element={<WeeklyBrief />} />
          <Route path="/actions" element={<Actions />} />
          <Route path="/audit" element={<Audit />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;