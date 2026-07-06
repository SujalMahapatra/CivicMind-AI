import React from "react";
import { cn } from "@/lib/utils";
import { Panel, StatusDot } from "./Primitives";
import { ArrowUpRight } from "lucide-react";

export const AgentStatusCard = ({ agent, onOpen }) => {
  const Icon = agent.icon;
  return (
    <Panel
      beam={agent.featured}
      className={cn(
        "group p-5 h-full flex flex-col justify-between",
        "transition-transform duration-300 ease-out hover:-translate-y-0.5",
        "hover:border-indigo-500/30"
      )}
      data-testid={`agent-card-${agent.id}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className={cn(
          "w-11 h-11 rounded-xl grid place-items-center",
          "bg-gradient-to-br", agent.accent,
          "shadow-[0_0_24px_rgba(79,70,229,0.25)]"
        )}>
          <Icon className="w-5 h-5 text-white" strokeWidth={1.6} />
        </div>
        <div className="flex items-center gap-2 rounded-full px-2.5 py-1 bg-white/[0.03] border border-white/10">
          <StatusDot status={agent.status} />
          <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-300">
            {agent.status}
          </span>
        </div>
      </div>

      <div className="mt-6">
        <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">
          {agent.role}
        </div>
        <h4 className="mt-1 font-display text-[17px] font-medium text-white tracking-tight">
          {agent.name}
        </h4>
        <p className="mt-1.5 text-[13px] leading-relaxed text-zinc-400">
          {agent.description}
        </p>
      </div>

      <div className="mt-6 pt-4 border-t border-white/[0.06] flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">Latency</div>
            <div className="text-sm text-zinc-200 font-mono">{agent.latency}</div>
          </div>
          <div className="h-8 w-px bg-white/10" />
          <div>
            <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">Calls</div>
            <div className="text-sm text-zinc-200 font-mono">{agent.calls.toLocaleString()}</div>
          </div>
        </div>
        <button
          data-testid={`agent-open-${agent.id}`}
          onClick={onOpen}
          className="inline-flex items-center gap-1 text-[12px] text-indigo-300 hover:text-indigo-200 transition-colors"
        >
          Open <ArrowUpRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </Panel>
  );
};

export default AgentStatusCard;
