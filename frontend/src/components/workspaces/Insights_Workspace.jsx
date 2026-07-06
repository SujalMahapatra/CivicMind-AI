import React, { useState, useEffect } from "react";
import { Panel, PanelHeader, SectionLabel, Chip } from "../civic/Primitives";
import { TypeWriter } from "../civic/TypeWriter";
import { Sparkles, RefreshCw, Copy, Check, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/button";
import api from "@/services/api";

const INSIGHT_TAGS = ["sanitation", "street-lighting", "north-district", "south-district", "sla-breach"];

export const InsightWorkspace = () => {
    const [runId, setRunId] = useState(0);
    const [copied, setCopied] = useState(false);

    const [insightText, setInsightText] = useState("");
    const [loading, setLoading] = useState(false);

    const [modelUsed, setModelUsed] = useState("");


    useEffect(() => {
        generateInsight();
    }, []);

    const generateInsight = async () => {
        try {
            setLoading(true);

            const response = await api.post(
                "/insight/generate",
                {
                    domain: "environment",

                    analytics_summary:
                        "Dataset contains 1000 rows with quality score 95 and 12 columns.",

                    prediction_summary:
                        "Temperature is expected to increase over the next 7 days with high confidence."
                }
            );

            setInsightText(
                response.data.insights
            );

            localStorage.setItem(
                "latest_insight",
                response.data.insights
            );

            setModelUsed(
                response.data.model_used
            );

            

        } catch (error) {
            console.error(
                "Insight generation failed:",
                error
            );
        } finally {
            setLoading(false);
        }
    };

    const copy = async () => {
        try {
            await navigator.clipboard.writeText(
                insightText
            );
            setCopied(true);
            setTimeout(() => setCopied(false), 1500);
        } catch (_e) { /* noop */ }
    };

    return (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
            <div className="xl:col-span-8">
                <Panel className="animate-in-up">
                    <PanelHeader
                        eyebrow="Insight Agent"
                        title="AI-generated narrative"
                        description="Synthesized from Analytics + Prediction runs and grounded in indexed civic policy."
                        actions={
                            <div className="flex items-center gap-2">
                                <Chip className="text-indigo-300 border-indigo-500/20 bg-indigo-500/10">
                                    <Sparkles className="w-3 h-3" /> {modelUsed || "Gemini"}
                                </Chip>
                                <Button
                                    data-testid="regenerate-insight-btn"
                                    size="sm"
                                    variant="outline"
                                    onClick={() => setRunId((n) => n + 1)}
                                    className="border-white/10 bg-white/[0.03] hover:bg-white/[0.08] text-white h-8"
                                >
                                    <RefreshCw className="w-3.5 h-3.5" /> Regenerate
                                </Button>
                                <Button
                                    data-testid="copy-insight-btn"
                                    size="sm"
                                    variant="outline"
                                    onClick={copy}
                                    className="border-white/10 bg-white/[0.03] hover:bg-white/[0.08] text-white h-8"
                                >
                                    {copied ? <><Check className="w-3.5 h-3.5" /> Copied</> : <><Copy className="w-3.5 h-3.5" /> Copy</>}
                                </Button>
                            </div>
                        }
                    />
                    <div className="px-6 pb-6">
                        <div
                            key={runId}
                            data-testid="insight-body"
                            className="relative rounded-xl border border-white/[0.06] bg-white/[0.02] p-6 border-l-2 border-l-indigo-500/60"
                        >
                            <TypeWriter
                                text={
                                    insightText ||
                                    "Generating AI insights..."
                                }
                                speed={8}
                            />
                        </div>

                        <div className="mt-5 flex flex-wrap gap-2">
                            {INSIGHT_TAGS.map((t) => (
                                <Chip key={t} className="font-mono">#{t}</Chip>
                            ))}
                        </div>
                    </div>
                </Panel>
            </div>

            {/* Insight facets */}
            <div className="xl:col-span-4 space-y-6">
                <Panel className="animate-in-up">
                    <PanelHeader eyebrow="What this means" title="Bottom line" />
                    <div className="px-6 pb-6 space-y-4">
                        <div className="rounded-xl border border-white/10 bg-white/[0.02] p-4">
                            <div className="flex items-center gap-2">
                                <Lightbulb className="w-4 h-4 text-amber-300" />
                                <div className="text-[11px] font-mono uppercase tracking-[0.2em] text-zinc-400">Primary driver</div>
                            </div>
                            <div className="mt-2 font-display text-lg text-white">Sanitation SLA gap</div>
                            <p className="mt-1 text-[13px] text-zinc-400">North + Central account for 34% volume and 41% of breaches this quarter.</p>
                        </div>

                        <div className="rounded-xl border border-white/10 bg-white/[0.02] p-4">
                            <div className="text-[11px] font-mono uppercase tracking-[0.2em] text-zinc-400">Projected outcome</div>
                            <div className="mt-2 font-display text-lg text-white">CSAT 3.8 → 3.5</div>
                            <p className="mt-1 text-[13px] text-zinc-400">If unaddressed, by end of month, given +4.6% resolution drift.</p>
                        </div>

                        <div className="rounded-xl border border-indigo-500/20 bg-indigo-500/10 p-4">
                            <div className="text-[11px] font-mono uppercase tracking-[0.2em] text-indigo-200">Recommended focus</div>
                            <div className="mt-2 font-display text-[15px] text-white leading-snug">
                                Reroute one sanitation crew to North + Central and audit Street Lighting in South wards 7, 9, 12.
                            </div>
                        </div>
                    </div>
                </Panel>
            </div>
        </div>
    );
};

export default InsightWorkspace;
