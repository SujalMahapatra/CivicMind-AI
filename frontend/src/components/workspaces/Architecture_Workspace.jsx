import React from "react";
import { Panel, PanelHeader, SectionLabel } from "../civic/Primitives";
import { TECH_STACK } from "@/lib/mock";
import { LineChart, Brain, Lightbulb, ListChecks, Database, MessagesSquare, Bot, ArrowDown } from "lucide-react";
import { cn } from "@/lib/utils";

const PIPELINE_A = [
    { key: "analytics", title: "Analytics", Icon: LineChart, tint: "from-sky-500 to-cyan-500" },
    { key: "prediction", title: "Prediction", Icon: Brain, tint: "from-blue-500 to-indigo-500" },
    { key: "insights", title: "Insights", Icon: Lightbulb, tint: "from-violet-500 to-fuchsia-500" },
    { key: "recommendations", title: "Recommendations", Icon: ListChecks, tint: "from-emerald-500 to-teal-500" },
];

const PIPELINE_B = [
    { key: "kb", title: "Knowledge Base", Icon: Database, tint: "from-indigo-500 to-blue-500" },
    { key: "rag", title: "RAG Assistant", Icon: MessagesSquare, tint: "from-cyan-500 to-blue-500" },
];

const PipelineNode = ({ node, index }) => {
    const { Icon, title, tint, key } = node;
    return (
        <div
            data-testid={`pipeline-node-${key}`}
            className="animate-in-up"
            style={{ animationDelay: `${index * 80}ms` }}
        >
            <Panel className="p-5">
                <div className="flex items-center gap-3">
                    <div className={cn("w-10 h-10 rounded-lg grid place-items-center bg-gradient-to-br", tint)}>
                        <Icon className="w-4 h-4 text-white" strokeWidth={1.6} />
                    </div>
                    <div>
                        <SectionLabel>Stage 0{index + 1}</SectionLabel>
                        <div className="font-display text-[15px] text-white">{title}</div>
                    </div>
                </div>
            </Panel>
        </div>
    );
};

const Arrow = () => (
    <div className="flex justify-center py-2">
        <ArrowDown className="w-4 h-4 text-indigo-300/70" />
    </div>
);

export const ArchitectureWorkspace = () => {
    return (
        <div className="space-y-6">
            <Panel className="p-6 md:p-8 animate-in-up beam">
                <PanelHeader
                    eyebrow="System topology"
                    title="Multi-agent decision flow"
                    description="Two pipelines cooperate: an analytics-driven decisioning path and a retrieval-grounded knowledge path, orchestrated by the Coordinator Agent."
                />
                <div className="px-2 md:px-6 pb-2 grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Coordinator anchor */}
                    <div className="md:col-span-2 flex justify-center">
                        <div className="w-full max-w-md">
                            <Panel beam className="p-5">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl grid place-items-center bg-gradient-to-br from-indigo-500 to-blue-500 shadow-[0_0_28px_rgba(79,70,229,0.4)]">
                                        <Bot className="w-5 h-5 text-white" strokeWidth={1.6} />
                                    </div>
                                    <div>
                                        <SectionLabel>Orchestrator</SectionLabel>
                                        <div className="font-display text-lg text-white">Coordinator Agent</div>
                                        <div className="text-[12px] text-zinc-400">Central orchestration layer for routing,
                                            workflow management and future agent collaboration.</div>
                                    </div>
                                </div>
                            </Panel>
                        </div>
                    </div>

                    {/* Pipeline A */}
                    <div>
                        <SectionLabel className="mb-3 text-center">Decision Pipeline</SectionLabel>
                        <div>
                            {PIPELINE_A.map((n, i) => (
                                <React.Fragment key={n.key}>
                                    <PipelineNode node={n} index={i} />
                                    {i < PIPELINE_A.length - 1 && <Arrow />}
                                </React.Fragment>
                            ))}
                        </div>
                    </div>

                    {/* Pipeline B */}
                    <div>
                        <SectionLabel className="mb-3 text-center">Knowledge Pipeline</SectionLabel>
                        <div>
                            {PIPELINE_B.map((n, i) => (
                                <React.Fragment key={n.key}>
                                    <PipelineNode node={n} index={i} />
                                    {i < PIPELINE_B.length - 1 && <Arrow />}
                                </React.Fragment>
                            ))}
                            <div className="mt-6 rounded-xl border border-dashed border-white/10 p-4 text-[12px] text-zinc-500 leading-relaxed">
                                Knowledge Base can be queried independently
                                through the RAG Assistant and serves as the
                                foundation for future grounded decision workflows.
                            </div>
                        </div>
                    </div>
                </div>
            </Panel>

            {/* Tech stack */}
            <Panel className="p-6 animate-in-up">
                <PanelHeader
                    eyebrow="Tech stack"
                    title="What powers CivicMind AI"
                    description="A modern, composable stack — production-ready and hackathon-friendly."
                />
                <div className="px-6 pb-6 grid grid-cols-2 md:grid-cols-5 gap-3">
                    {TECH_STACK.map((t) => (
                        <div
                            key={t.name}
                            data-testid={`arch-tech-${t.name.toLowerCase()}`}
                            className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4 hover:border-indigo-500/30 transition-colors"
                        >
                            <div className={cn("font-display text-[15px] font-medium", t.color)}>{t.name}</div>
                            <div className="mt-1 text-[11px] text-zinc-500">{t.tag}</div>
                        </div>
                    ))}
                </div>
            </Panel>
        </div>
    );
};

export default ArchitectureWorkspace;
