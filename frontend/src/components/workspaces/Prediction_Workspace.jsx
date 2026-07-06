import React, { useState } from "react";
import { Panel, PanelHeader, SectionLabel, StatChip, Chip } from "../civic/Primitives";
import { PREDICTION_RESULT, SAMPLE_DATASET } from "@/lib/mock";
import { Play, Loader2, TrendingUp, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import api from "@/services/api";

const NUMERIC_COLUMNS = ["resolution_hours", "satisfaction", "ticket_id"];

export const PredictionWorkspace = () => {
  const [target, setTarget] = useState("resolution_hours");
  const [horizon, setHorizon] = useState(14);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);

  const runForecast = async () => {
  try {
    setRunning(true);
    setResult(null);

    const formData = new FormData();

    formData.append(
      "file",
      selectedFile
    );

    formData.append(
      "target_column",
      target
    );

    formData.append(
      "forecast_days",
      horizon
    );

    const response = await api.post(
      "/prediction/forecast",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    );

    const data = response.data;

    setResult({
      target: data.target_column,
      horizon: data.forecast_days,
      confidence: data.r2_score,
      trend: data.trend_direction,

      forecast: data.predictions.map(
        (value, index) => ({
          day: `D+${index + 1}`,
          value,
          lower: value * 0.95,
          upper: value * 1.05
        })
      ),

      model: data.model_used
    });

  } catch (error) {
    console.error(error);
  } finally {
    setRunning(false);
  }
};

  const maxVal = result ? Math.max(...result.forecast.map(f => f.upper)) : 0;
  const minVal = result ? Math.min(...result.forecast.map(f => f.lower)) : 0;
  const range = maxVal - minVal || 1;

  return (
    <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
      {/* CONFIG */}
      <div className="xl:col-span-4">
        <Panel className="animate-in-up">
          <PanelHeader
            eyebrow="Configure forecast"
            title="Prediction inputs"
            description="Prediction Agent uses a calibrated time-series model. Choose your target and horizon."
          />
          <div className="px-6 pb-6 space-y-5">
            <div className="space-y-2">
              <Label htmlFor="target-col" className="text-[11px] font-mono uppercase tracking-[0.2em] text-zinc-400">
                Target column
              </Label>
              <Select value={target} onValueChange={setTarget}>
                <SelectTrigger
                  id="target-col"
                  data-testid="target-column-select"
                  className="bg-white/[0.03] border-white/10 text-white h-10"
                >
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-[#0A0A12] border-white/10 text-white">
                  {NUMERIC_COLUMNS.map((c) => (
                    <SelectItem key={c} value={c} className="font-mono">{c}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-[11px] text-zinc-500">Detected numeric columns from the last dataset.</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="horizon" className="text-[11px] font-mono uppercase tracking-[0.2em] text-zinc-400">
                Forecast horizon (days)
              </Label>
              <Input
                id="horizon"
                data-testid="forecast-horizon-input"
                type="number"
                min={1}
                max={90}
                value={horizon}
                onChange={(e) => setHorizon(e.target.value)}
                className="bg-white/[0.03] border-white/10 text-white h-10 font-mono"
              />
              <div className="flex gap-2 pt-1">
                {[7, 14, 30, 60].map((n) => (
                  <button
                    key={n}
                    data-testid={`horizon-preset-${n}`}
                    onClick={() => setHorizon(n)}
                    className={`text-[11px] font-mono px-2.5 py-1 rounded-md border transition-colors ${
                      Number(horizon) === n
                        ? "border-indigo-500/50 text-indigo-200 bg-indigo-500/10"
                        : "border-white/10 text-zinc-400 hover:text-white hover:bg-white/[0.04]"
                    }`}
                  >
                    {n}d
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <Label className="text-[11px] font-mono uppercase tracking-[0.2em] text-zinc-400">
                Model
              </Label>
              <div className="rounded-xl border border-white/10 bg-white/[0.02] p-3 flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-500 grid place-items-center">
                  <Sparkles className="w-4 h-4 text-white" strokeWidth={1.6} />
                </div>
                <div>
                  <div className="text-sm text-white">Ensemble · Trend + Seasonal</div>
                  <div className="text-[11px] text-zinc-500 font-mono">gemini-reasoner · 86% avg. confidence</div>
                </div>
              </div>
            </div>

            <Button
              data-testid="run-forecast-btn"
              onClick={runForecast}
              disabled={running || !target}
              className="w-full bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white border-0 shadow-[0_0_28px_rgba(79,70,229,0.35)]"
            >
              {running ? <><Loader2 className="w-4 h-4 animate-spin" /> Forecasting…</> : <><Play className="w-4 h-4" /> Run forecast</>}
            </Button>
          </div>
        </Panel>
      </div>

      {/* RESULTS */}
      <div className="xl:col-span-8">
        <Panel className="animate-in-up min-h-[420px]">
          <PanelHeader
            eyebrow="Forecast"
            title="Prediction results"
            description="Point estimate with 90% confidence bands."
            actions={result ? <Chip className="text-emerald-300 border-emerald-500/20 bg-emerald-500/10"><TrendingUp className="w-3 h-3" />confidence {(result.confidence * 100).toFixed(0)}%</Chip> : null}
          />
          <div className="px-6 pb-6">
            {!result && !running && (
              <div className="rounded-xl border border-dashed border-white/10 p-10 text-center">
                <div className="font-display text-white text-lg">No forecast yet</div>
                <p className="mt-1 text-sm text-zinc-500">Choose a target column and press <span className="font-mono text-zinc-300">Run forecast</span>.</p>
              </div>
            )}
            {running && (
              <div className="rounded-xl border border-white/10 p-10 flex items-center gap-4">
                <Loader2 className="w-5 h-5 animate-spin text-indigo-300" />
                <div>
                  <div className="text-white text-sm">Prediction Agent is fitting the model…</div>
                  <div className="text-[12px] text-zinc-500 font-mono">decomposing · fitting · calibrating intervals</div>
                </div>
              </div>
            )}
            {result && (
              <div className="space-y-6">
                <p className="text-[15px] text-zinc-200 leading-relaxed border-l-2 border-indigo-500/60 pl-4">
                  {result.trend}
                </p>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <StatChip label="Target" value={<span className="font-mono text-[15px]">{result.target}</span>} />
                  <StatChip label="Horizon" value={`${result.horizon}d`} />
                  <StatChip label="Confidence" value={`${(result.confidence * 100).toFixed(0)}%`} />
                  <StatChip label="Model" value="Ensemble" hint="trend+seasonal" />
                </div>

                {/* Chart */}
                <div>
                  <SectionLabel className="mb-3">Forecast curve</SectionLabel>
                  <div className="rounded-xl border border-white/10 bg-white/[0.02] p-5">
                    <div className="relative h-56">
                      <svg viewBox="0 0 800 220" preserveAspectRatio="none" className="w-full h-full">
                        <defs>
                          <linearGradient id="areaGrad" x1="0" x2="0" y1="0" y2="1">
                            <stop offset="0%" stopColor="#6366F1" stopOpacity="0.5" />
                            <stop offset="100%" stopColor="#6366F1" stopOpacity="0" />
                          </linearGradient>
                          <linearGradient id="lineGrad" x1="0" x2="1" y1="0" y2="0">
                            <stop offset="0%" stopColor="#818CF8" />
                            <stop offset="100%" stopColor="#22D3EE" />
                          </linearGradient>
                        </defs>
                        {/* grid */}
                        {[0.25, 0.5, 0.75].map((p, i) => (
                          <line key={i} x1="0" x2="800" y1={220 * p} y2={220 * p}
                            stroke="rgba(255,255,255,0.05)" strokeDasharray="3 4" />
                        ))}
                        {(() => {
                          const n = result.forecast.length;
                          const x = (i) => (i / (n - 1)) * 800;
                          const y = (v) => 220 - ((v - minVal) / range) * 200 - 10;
                          const upperPath = result.forecast.map((f, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(f.upper)}`).join(" ");
                          const lowerPath = result.forecast.slice().reverse().map((f, i) => `L ${x(n - 1 - i)} ${y(f.lower)}`).join(" ");
                          const line = result.forecast.map((f, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(f.value)}`).join(" ");
                          return (
                            <>
                              <path d={`${upperPath} ${lowerPath} Z`} fill="url(#areaGrad)" opacity="0.6" />
                              <path d={line} fill="none" stroke="url(#lineGrad)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                              {result.forecast.map((f, i) => (
                                <circle key={i} cx={x(i)} cy={y(f.value)} r="2.5" fill="#E0E7FF" opacity="0.9" />
                              ))}
                            </>
                          );
                        })()}
                      </svg>
                    </div>
                    <div className="mt-2 flex justify-between text-[10px] font-mono text-zinc-500">
                      <span>{result.forecast[0].day}</span>
                      <span>{result.forecast[Math.floor(result.forecast.length / 2)].day}</span>
                      <span>{result.forecast[result.forecast.length - 1].day}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </Panel>
      </div>
    </div>
  );
};

export default PredictionWorkspace;
