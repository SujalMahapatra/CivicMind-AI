
import React from "react";
import {
  LayoutDashboard, LineChart, Brain, Lightbulb, ListChecks,
  MessagesSquare, Workflow, ChevronLeft, ChevronRight, Radio,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { key: "overview",       label: "Overview",           icon: LayoutDashboard },
  { key: "analytics",      label: "Analytics",          icon: LineChart },
  { key: "prediction",     label: "Prediction",         icon: Brain },
  { key: "insight",        label: "Insights",           icon: Lightbulb },
  { key: "recommendation", label: "Recommendations",    icon: ListChecks },
  { key: "knowledge",      label: "Knowledge Assistant",icon: MessagesSquare },
  { key: "architecture",   label: "Architecture",       icon: Workflow },
];

export const Sidebar = ({ active, onChange, collapsed, onToggle }) => {
  return (
    <aside
      data-testid="app-sidebar"
      className={cn(
        "relative z-10 shrink-0 h-full flex flex-col",
        "glass border-r border-white/5",
        collapsed ? "w-[76px]" : "w-[260px]",
        "transition-[width] duration-300 ease-out"
      )}
    >
      {/* Brand */}
      <div className="h-16 px-4 flex items-center gap-3 border-b border-white/5">
        <div className="relative shrink-0">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-blue-500 grid place-items-center shadow-[0_0_24px_rgba(79,70,229,0.4)]">
            <Radio className="w-4 h-4 text-white" strokeWidth={2} />
          </div>
          <span className="absolute -bottom-1 -right-1 pulse-dot" />
        </div>
        {!collapsed && (
          <div className="flex flex-col leading-tight">
            <span className="font-display text-[15px] font-semibold tracking-tight text-white">CivicMind</span>
            <span className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">AI · v0.1</span>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1">
        {!collapsed && (
          <div className="px-2 pt-2 pb-3 text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">
            Workspaces
          </div>
        )}
        {NAV.map((item, idx) => {
          const Icon = item.icon;
          const isActive = active === item.key;
          return (
            <button
              key={item.key}
              data-testid={`nav-${item.key}`}
              onClick={() => onChange(item.key)}
              className={cn(
                "group relative w-full flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm",
                "transition-all duration-200 outline-none",
                "focus-visible:ring-2 focus-visible:ring-indigo-500/60",
                isActive
                  ? "bg-white/[0.06] text-white ring-1 ring-inset ring-indigo-500/30"
                  : "text-zinc-400 hover:text-white hover:bg-white/[0.04]"
              )}
              style={{ animationDelay: `${idx * 30}ms` }}
            >
              <span className={cn(
                "shrink-0 grid place-items-center w-7 h-7 rounded-lg transition-colors",
                isActive
                  ? "bg-gradient-to-br from-indigo-500/30 to-blue-500/20 text-indigo-200"
                  : "bg-white/[0.03] text-zinc-400 group-hover:text-white"
              )}>
                <Icon className="w-4 h-4" strokeWidth={1.6} />
              </span>
              {!collapsed && <span className="truncate">{item.label}</span>}
              {isActive && (
                <span className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-400 shadow-[0_0_10px_rgba(129,140,248,0.9)]" />
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-white/5">
        <button
          data-testid="sidebar-toggle"
          onClick={onToggle}
          className="w-full flex items-center justify-center gap-2 rounded-xl px-3 py-2 text-xs font-mono uppercase tracking-[0.2em] text-zinc-400 hover:text-white hover:bg-white/[0.04] transition-colors"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <>
            <ChevronLeft className="w-4 h-4" />
            <span>Collapse</span>
          </>}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
