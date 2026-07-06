import React, { useMemo, useState } from "react";
import { Panel, PanelHeader, SectionLabel, Chip } from "../civic/Primitives";
import { CheckCircle2, ChevronRight, TrendingUp, Gauge, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import api from "@/services/api";

const IMPACT_COLOR = {
    High: "text-emerald-300 bg-emerald-500/10 border-emerald-500/20",
    Medium: "text-amber-300 bg-amber-500/10 border-amber-500/20",
    Low: "text-zinc-300 bg-white/[0.04] border-white/10",
};

export const RecommendationWorkspace = () => {
    const [activeCategory, setActiveCategory] = useState("All");
    const [selected, setSelected] = useState(RECOMMENDATIONS[0].id);

    const categories = useMemo(() => ["All", ...ACTION_CATEGORIES.map(c => c.key)], []);

    const filtered = useMemo(
        () => activeCategory === "All"
            ? RECOMMENDATIONS
            : RECOMMENDATIONS.filter(r => r.category === activeCategory),
        [activeCategory]
    );

    const active = RECOMMENDATIONS.find(r => r.id === selected) || RECOMMENDATIONS[0];

    const generateRecommendations = async () => {
        try {
            setLoading(true);

            const response = await api.post(
                "/recommendation/generate",
                {
                    domain: "environment",

                    insights:
                        "AQI is expected to increase significantly over the next week and may impact community health."
                }
            );

            setRecommendationText(
                response.data.recommendations
            );

            setModelUsed(
                response.data.model_used
            );

        } catch (error) {
            console.error(
                "Recommendation generation failed",
                error
            );
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        generateRecommendations();
    }, []);
    return (
        <div className="space-y-6">
            {/* Category filter row */}
            <Panel className="p-4 animate-in-up">
                <div className="flex flex-wrap items-center gap-2">
                    <SectionLabel className="mr-2">Action categories</SectionLabel>
                    {categories.map((c) => {
                        const cfg = ACTION_CATEGORIES.find(a => a.key === c);
                        const isActive = activeCategory === c;
                        return (
                            <button
                                key={c}
                                data-testid={`category-${c.toLowerCase()}`}
                                onClick={() => setActiveCategory(c)}
                                className={cn(
                                    "inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-[12px] font-medium border transition-colors",
                                    isActive
                                        ? "border-indigo-500/50 text-white bg-indigo-500/10"
                                        : "border-white/10 text-zinc-400 hover:text-white hover:bg-white/[0.05]"
                                )}
                            >
                                {cfg && <span className={cn("w-1.5 h-1.5 rounded-full", cfg.bg.replace("bg-", "bg-"))} />}
                                {c}
                                <span className="text-[10px] font-mono text-zinc-500">
                                    {c === "All" ? RECOMMENDATIONS.length : RECOMMENDATIONS.filter(r => r.category === c).length}
                                </span>
                            </button>
                        );
                    })}
                </div>
            </Panel>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
                {/* LIST */}
                <div className="xl:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-4">
                    {filtered.map((r, i) => {
                        const cfg = ACTION_CATEGORIES.find(a => a.key === r.category);
                        const isSelected = r.id === selected;
                        return (
                            <button
                                key={r.id}
                                data-testid={`rec-card-${r.id}`}
                                onClick={() => setSelected(r.id)}
                                className={cn(
                                    "text-left rounded-2xl p-5 border transition-all animate-in-up",
                                    "bg-[#0A0A12]/70 backdrop-blur-xl",
                                    "hover:-translate-y-0.5",
                                    isSelected
                                        ? "border-indigo-500/40 ring-1 ring-inset ring-indigo-500/30 shadow-[0_0_36px_-8px_rgba(79,70,229,0.4)]"
                                        : "border-white/[0.06] hover:border-white/15"
                                )}
                                style={{ animationDelay: `${i * 60}ms` }}
                            >
                                <div className="flex items-center justify-between">
                                    <Chip className={cn(cfg?.bg, cfg?.color, "border-white/10")}>
                                        {r.category}
                                    </Chip>
                                    <Chip className={IMPACT_COLOR[r.impact]}>{r.impact} impact</Chip>
                                </div>
                                <h4 className="mt-4 font-display text-[16px] font-medium text-white leading-snug">
                                    {r.title}
                                </h4>
                                <p className="mt-2 text-[13px] text-zinc-400 leading-relaxed">{r.description}</p>
                                <div className="mt-4 flex items-center gap-4 text-[11px] font-mono text-zinc-500">
                                    <span className="inline-flex items-center gap-1"><Gauge className="w-3.5 h-3.5" /> {r.effort} effort</span>
                                    <span className="inline-flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {r.timeframe}</span>
                                </div>
                            </button>
                        );
                    })}
                </div>

                {/* DETAIL */}
                <div className="xl:col-span-5">
                    <Panel className="animate-in-up" beam>
                        <PanelHeader
                            eyebrow="Details"
                            title={active.title}
                            description={active.description}
                        />
                        <div className="px-6 pb-6 space-y-5">
                            <div className="rounded-xl border border-indigo-500/20 bg-indigo-500/10 p-4">
                                <div className="flex items-center gap-2">
                                    <TrendingUp className="w-4 h-4 text-indigo-200" />
                                    <div className="text-[11px] font-mono uppercase tracking-[0.2em] text-indigo-200">Expected outcome</div>
                                </div>
                                <div className="mt-2 font-display text-lg text-white">{active.expectedOutcome}</div>
                            </div>

                            <div className="grid grid-cols-3 gap-3">
                                <div className="rounded-xl border border-white/10 bg-white/[0.02] p-3">
                                    <SectionLabel>Impact</SectionLabel>
                                    <div className="mt-1 text-sm text-white">{active.impact}</div>
                                </div>
                                <div className="rounded-xl border border-white/10 bg-white/[0.02] p-3">
                                    <SectionLabel>Effort</SectionLabel>
                                    <div className="mt-1 text-sm text-white">{active.effort}</div>
                                </div>
                                <div className="rounded-xl border border-white/10 bg-white/[0.02] p-3">
                                    <SectionLabel>Timeframe</SectionLabel>
                                    <div className="mt-1 text-sm text-white">{active.timeframe}</div>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <SectionLabel>Suggested plan</SectionLabel>
                                <ul className="space-y-2">
                                    {[
                                        "Identify owning department and assign a lead",
                                        "Prepare data brief + baseline metrics",
                                        "Execute pilot on a bounded scope",
                                        "Measure impact vs. baseline within timeframe",
                                    ].map((step, i) => (
                                        <li key={i} className="flex items-start gap-2 text-[13px] text-zinc-300">
                                            <CheckCircle2 className="w-4 h-4 mt-0.5 text-emerald-300 shrink-0" />
                                            <span>{step}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <button
                                data-testid="rec-promote-btn"
                                className="w-full inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white shadow-[0_0_28px_rgba(79,70,229,0.35)]"
                            >
                                Promote to action queue <ChevronRight className="w-4 h-4" />
                            </button>
                        </div>
                    </Panel>
                </div>
            </div>
        </div>
    );
};

export default RecommendationWorkspace;
