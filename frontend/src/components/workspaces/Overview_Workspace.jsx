import React from "react";
import { Panel, PanelHeader, StatChip, SectionLabel, Chip } from "../civic/Primitives";
import { AgentStatusCard } from "../civic/AgentStatusCard";
import { AGENTS, TECH_STACK } from "@/lib/mock";
import { ArrowRight, Zap, TrendingUp, Users, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";

const KPIs = [
  { label: "Active decisions", value: "24", hint: "+3 today", icon: Zap },
  { label: "Citizens impacted", value: "182K", hint: "estimated reach", icon: Users },
  { label: "Prediction confidence", value: "86%", hint: "avg. across runs", icon: TrendingUp },
  { label: "Policy grounding", value: "1,204", hint: "docs indexed", icon: ShieldCheck },
];

export const OverviewWorkspace = ({ onGoto }) => {
  return (
    <div className="space-y-8">
      {/* Hero */}
      <Panel className="relative overflow-hidden p-8 md:p-10 animate-in-up">
        <div className="absolute inset-0 -z-10 opacity-70 pointer-events-none">
          <div className="absolute -top-24 -left-24 w-[420px] h-[420px] rounded-full bg-indigo-500/20 blur-3xl" />
          <div className="absolute -bottom-24 -right-24 w-[360px] h-[360px] rounded-full bg-cyan-500/15 blur-3xl" />
        </div>
        <div className="max-w-3xl">
          <SectionLabel>Multi-Agent · Civic Intelligence</SectionLabel>
          <h2 className="mt-3 font-display text-3xl md:text-5xl font-semibold tracking-tight text-white leading-[1.05]">
            Better civic decisions,{" "}
            <span className="text-gradient">grounded in data</span>{" "}
            and orchestrated by agents.
          </h2>
          <p className="mt-4 text-[15px] text-zinc-400 leading-relaxed">
            Six specialized agents — Coordinator, Analytics, Prediction, Insight, Recommendation and RAG — cooperate to turn into actionable, transparent outcomes for smarter community decision-making.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button
              data-testid="hero-run-analysis"
              onClick={() => onGoto("analytics")}
              className="bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white border-0 shadow-[0_0_28px_rgba(79,70,229,0.35)]"
            >
              Run new analysis <ArrowRight className="w-4 h-4" />
            </Button>
            <Button
              data-testid="hero-ask-assistant"
              variant="outline"
              onClick={() => onGoto("knowledge")}
              className="border-white/10 bg-white/[0.03] hover:bg-white/[0.06] text-white"
            >
              Ask the Knowledge Assistant
            </Button>
          </div>
        </div>
      </Panel>

      {/* KPIs */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {KPIs.map((k, i) => {
          const Icon = k.icon;
          return (
            <Panel key={k.label} className="p-5 animate-in-up" style={{ animationDelay: `${i * 60}ms` }}>
              <div className="flex items-center justify-between">
                <SectionLabel>{k.label}</SectionLabel>
                <Icon className="w-4 h-4 text-indigo-300" strokeWidth={1.6} />
              </div>
              <div className="mt-2 font-display text-3xl text-white tracking-tight">{k.value}</div>
              <div className="mt-1 text-[11px] text-zinc-500">{k.hint}</div>
            </Panel>
          );
        })}
      </div>

      {/* Agents Bento */}
      <div>
        <div className="flex items-end justify-between mb-4">
          <div>
            <SectionLabel>Agent Network</SectionLabel>
            <h3 className="mt-1 font-display text-xl text-white tracking-tight">Live agent status</h3>
          </div>
          <Chip>
            <span className="pulse-dot" />
            Realtime
          </Chip>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          {AGENTS.map((a, i) => (
            <div key={a.id} className="animate-in-up" style={{ animationDelay: `${i * 80}ms` }}>
              <AgentStatusCard
                agent={a}
                onOpen={() => {
                  if (a.id === "coordinator") onGoto("architecture");
                  else if (a.id === "rag") onGoto("knowledge");
                  else onGoto(a.id);
                }}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Tech stack strip */}
      <Panel className="p-6 animate-in-up">
        <PanelHeader
          eyebrow="Stack"
          title="Built with a modern AI stack"
          description="Every layer is composable and swappable — Built using FastAPI, Gemini, ChromaDB, and React to support scalable AI-powered decision intelligence."
        />
        <div className="px-6 pb-6 grid grid-cols-2 md:grid-cols-5 gap-3">
          {TECH_STACK.map((t) => (
            <div
              key={t.name}
              data-testid={`tech-${t.name.toLowerCase()}`}
              className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4 hover:border-indigo-500/30 transition-colors"
            >
              <div className={`font-display text-[15px] font-medium ${t.color}`}>{t.name}</div>
              <div className="mt-1 text-[11px] text-zinc-500">{t.tag}</div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
};

export default OverviewWorkspace;
