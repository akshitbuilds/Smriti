import React from "react";
import {
  LayoutDashboard,
  MessageCircleQuestion,
  ListChecks,
  GitBranch,
  AlertTriangle,
  FileText,
  Zap,
  ClipboardList,
} from "lucide-react";

const items = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },

  {
    id: "ask",
    label: "Ask Smriti",
    icon: MessageCircleQuestion,
  },

  {
    id: "commitments",
    label: "Commitments",
    icon: ListChecks,
  },

  {
    id: "decisions",
    label: "Decisions",
    icon: GitBranch,
  },

  {
    id: "conflicts",
    label: "Conflicts",
    icon: AlertTriangle,
  },

  {
    id: "weekly",
    label: "Weekly Brief",
    icon: FileText,
  },

  {
    id: "actions",
    label: "Actions",
    icon: Zap,
  },

  {
    id: "audit",
    label: "Audit Log",
    icon: ClipboardList,
  },
];

export default function Sidebar({ page, setPage }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-logo">S</div>

        <div>
          <h2>SMRITI</h2>
          <span>Sovereign Team Memory</span>
        </div>
      </div>

      <nav>
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              className={`nav-item ${
                page === item.id ? "active" : ""
              }`}
              onClick={() => setPage(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <span className="local-dot"></span>
        LOCAL MODE
      </div>
    </aside>
  );
}