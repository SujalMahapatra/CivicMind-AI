import React from "react";
import { Search, Command, Bell, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

const TITLES = {
  overview:       { title: "Mission Control",        subtitle: "Real-time status across the multi-agent civic decision network." },
  analytics:      { title: "Analytics Workspace",    subtitle: "Profile civic datasets and surface distributions, anomalies and drivers." },
  prediction:     { title: "Prediction Workspace",   subtitle: "Forecast civic outcomes with calibrated confidence intervals." },
  insight:        { title: "Insight Workspace",      subtitle: "AI-synthesized narratives grounded in analytics + forecasts." },
  recommendation: { title: "Recommendation Workspace", subtitle: "Prioritized, actionable interventions with impact and effort." },
  knowledge:      { title: "Knowledge Assistant",    subtitle: "Ask anything — answers grounded in indexed civic knowledge." },
  architecture:   { title: "System Architecture",    subtitle: "Data flow across agents, retrieval and reasoning layers." },
};

export const Header = ({ active }) => {
  const { title, subtitle } = TITLES[active] || TITLES.overview;
  return (
    <header
      data-testid="app-header"
      className="relative z-10 h-16 px-6 md:px-8 flex items-center gap-4 border-b border-white/5 glass-strong"
    >
      <div className="min-w-0">
        <div className="flex items-center gap-3">
          <span className="text-[10px] font-mono uppercase tracking-[0.3em] text-indigo-300/80">CIVICMIND · AI</span>
          <span className="hidden sm:inline-block h-3 w-px bg-white/10" />
          <span className="hidden sm:inline-block text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">
            {active}
          </span>
        </div>
        <h1 className="font-display text-lg md:text-xl font-medium tracking-tight text-white truncate">
          {title}
        </h1>
      </div>

      <div className="hidden md:flex ml-4 flex-1 max-w-xl">
        <div
          data-testid="global-search"
          className="w-full flex items-center gap-3 rounded-xl px-3.5 py-2 bg-white/[0.03] border border-white/10 hover:border-white/20 transition-colors focus-within:border-indigo-500/50 focus-within:ring-2 focus-within:ring-indigo-500/20"
        >
          <Search className="w-4 h-4 text-zinc-500" strokeWidth={1.6} />
          <input
            className="flex-1 bg-transparent outline-none text-sm placeholder:text-zinc-500 text-white"
            placeholder="Search across agents, datasets, insights..."
            aria-label="Global search"
          />
          <span className="hidden lg:inline-flex items-center gap-1 text-[10px] font-mono text-zinc-500 border border-white/10 rounded-md px-1.5 py-0.5">
            <Command className="w-3 h-3" /> K
          </span>
        </div>
      </div>

      <div className="ml-auto flex items-center gap-2">
        <div className="hidden sm:flex items-center gap-2 rounded-full pl-2 pr-3 py-1 bg-white/[0.03] border border-white/10">
          <span className="pulse-dot" />
          <span className="text-[11px] font-mono text-zinc-300">All agents online</span>
        </div>

        <Button
          data-testid="new-run-btn"
          className="hidden md:inline-flex bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white border-0 shadow-[0_0_24px_rgba(79,70,229,0.35)]"
          size="sm"
        >
          <Sparkles className="w-4 h-4" strokeWidth={1.8} />
          New Run
        </Button>

        <button
          data-testid="header-notifications"
          className="relative w-9 h-9 grid place-items-center rounded-xl bg-white/[0.03] border border-white/10 hover:border-white/20 text-zinc-300 hover:text-white transition-colors"
          aria-label="Notifications"
        >
          <Bell className="w-4 h-4" strokeWidth={1.6} />
          <span className="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-indigo-400" />
        </button>

        <div
          data-testid="header-avatar"
          className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 via-blue-500 to-cyan-500 grid place-items-center text-[11px] font-semibold text-white shadow-[0_0_16px_rgba(59,130,246,0.35)]"
          title="Analyst"
        >
          CM
        </div>
      </div>

      {/* subtle subtitle in second row for desktop only */}
      <p className="hidden xl:block absolute left-8 bottom-1.5 text-[11px] text-zinc-500 truncate max-w-[80%]">
        {subtitle}
      </p>
    </header>
  );
};

export default Header;
