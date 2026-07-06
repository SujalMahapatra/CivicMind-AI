import React, { useEffect, useState } from "react";
import { Panel, PanelHeader } from "../civic/Primitives";
import { ChevronRight, Loader2 } from "lucide-react";
import api from "@/services/api";
const IMPACT_COLOR = {
    High: "text-emerald-300 bg-emerald-500/10 border-emerald-500/20",
    Medium: "text-amber-300 bg-amber-500/10 border-amber-500/20",
    Low: "text-zinc-300 bg-white/[0.04] border-white/10",
};

export const RecommendationWorkspace = () => {
    const [loading, setLoading] = useState(false);

    const [recommendationText, setRecommendationText] = useState("");

    const [modelUsed, setModelUsed] = useState("");

    const [insightText, setInsightText] = useState("");
    useEffect(() => {
        const savedInsight =
            localStorage.getItem("latest_insight");

        if (savedInsight) {
            setInsightText(savedInsight);
        }
    }, []);
    
    const generateRecommendations = async () => {
        if (!insightText.trim()) return;

        try {
            setLoading(true);

            const response = await api.post(
                "/recommendation/generate",
                {
                    domain: "environment",
                    insights: insightText
                }
            );

            setRecommendationText(
                response.data.recommendations
            );

            setModelUsed(
                response.data.model_used
            );

        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        if (insightText) {
            generateRecommendations();
        }
    }, [insightText]);
    return (
        <div className="space-y-6">

            <Panel>
                <PanelHeader
                    eyebrow="Recommendation Agent"
                    title="AI Generated Recommendations"
                    description="Generated from Insight Agent output"
                />

                <div className="p-6">

                    <div className="mb-4">
                        <h3 className="text-white font-semibold mb-2">
                            Insight Received
                        </h3>

                        <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4 text-zinc-300">
                            {insightText || "No insight available"}
                        </div>
                    </div>

                    <button
                        onClick={generateRecommendations}
                        disabled={loading}
                        className="inline-flex items-center gap-2 rounded-xl px-4 py-2 bg-gradient-to-r from-indigo-500 to-blue-500 text-white"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Generating...
                            </>
                        ) : (
                            <>
                                Generate Recommendations
                                <ChevronRight className="w-4 h-4" />
                            </>
                        )}
                    </button>

                </div>
            </Panel>

            {recommendationText && (
                <Panel>

                    <PanelHeader
                        eyebrow="Output"
                        title="Recommended Actions"
                    />

                    <div className="p-6">

                        <div className="rounded-xl border border-indigo-500/20 bg-indigo-500/10 p-5 whitespace-pre-wrap text-zinc-200">
                            {recommendationText}
                        </div>

                        <div className="mt-4 text-sm text-zinc-500">
                            Model Used: {modelUsed}
                        </div>

                    </div>

                </Panel>
            )}

        </div>
    );
};
export default RecommendationWorkspace;