import { NavLink } from "react-router-dom";
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
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard, path: "/" },
  { id: "ask", label: "Ask Smriti", icon: MessageCircleQuestion, path: "/ask" },
  { id: "commitments", label: "Commitments", icon: ListChecks, path: "/commitments" },
  { id: "decisions", label: "Decisions", icon: GitBranch, path: "/decisions" },
  { id: "conflicts", label: "Conflicts", icon: AlertTriangle, path: "/conflicts" },
  { id: "weekly", label: "Weekly Brief", icon: FileText, path: "/weekly-brief" },
  { id: "actions", label: "Actions", icon: Zap, path: "/actions" },
  { id: "audit", label: "Audit Log", icon: ClipboardList, path: "/audit" },
];

export default function Sidebar() {
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
            <NavLink
              key={item.id}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
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