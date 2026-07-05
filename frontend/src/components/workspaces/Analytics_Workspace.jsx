import React, { useCallback, useMemo, useState } from "react";
import { Panel, PanelHeader, SectionLabel, StatChip, Chip } from "../civic/Primitives";
import { SAMPLE_DATASET, ANALYSIS_RESULTS } from "@/lib/mock";
import { Upload, FileSpreadsheet, CheckCircle2, Loader2, AlertTriangle, X, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";
import api from "@/services/api";

const SEVERITY_COLOR = {
    high: "text-rose-300 bg-rose-500/10 border-rose-500/20",
    medium: "text-amber-300 bg-amber-500/10 border-amber-500/20",
    low: "text-emerald-300 bg-emerald-500/10 border-emerald-500/20",
};

export const AnalyticsWorkspace = () => {
    const [dataset, setDataset] = useState(null);         // { name, rows, cols, size }
    const [dragging, setDragging] = useState(false);
    const [running, setRunning] = useState(false);
    const [results, setResults] = useState(null);

    const onFile = useCallback((file) => {
        if (!file) return;
        // We don't parse the file — we mimic profiling with the sample dataset.
        setDataset({
            file,
            name: file.name,
            size: `${(file.size / 1024 / 1024).toFixed(2)} MB`
        });
        setResults(null);
    }, []);

    const onDrop = (e) => {
        e.preventDefault(); setDragging(false);
        const f = e.dataTransfer.files?.[0];
        if (f) onFile(f);
    };

    const loadSample = () => {
        setDataset({ name: SAMPLE_DATASET.name, rows: SAMPLE_DATASET.rows, cols: SAMPLE_DATASET.cols, size: SAMPLE_DATASET.size });
        setResults(null);
    };

    const runAnalysis = async () => {
        if (!dataset?.file) return;

        try {
            setRunning(true);

            const formData = new FormData();

            formData.append(
                "file",
                dataset.file
            );

            const response = await api.post(
                "/analytics/analyze",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            setResults(response.data);

        } catch (error) {
            console.error(error);
        } finally {
            setRunning(false);
        }
    };
};
const maxDist = useMemo(() => Math.max(...ANALYSIS_RESULTS.distribution.map(d => d.value)), []);

return (
    <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        {/* LEFT: upload + preview */}
        <div className="xl:col-span-5 space-y-6">
            <Panel className="animate-in-up">
                <PanelHeader
                    eyebrow="Step 01 · Dataset"
                    title="Upload a civic dataset"
                    description="CSV or Excel. Analytics Agent profiles distributions, quality and anomalies."
                />
                <div className="px-6 pb-6">
                    <label
                        data-testid="dropzone"
                        htmlFor="analytics-file-input"
                        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                        onDragLeave={() => setDragging(false)}
                        onDrop={onDrop}
                        className={cn(
                            "relative flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed p-8 cursor-pointer transition-all",
                            dragging
                                ? "border-indigo-500/60 bg-indigo-500/[0.06]"
                                : "border-white/10 hover:border-white/25 hover:bg-white/[0.02]"
                        )}
                    >
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500/30 to-blue-500/20 grid place-items-center">
                            <Upload className="w-5 h-5 text-indigo-200" strokeWidth={1.6} />
                        </div>
                        <div className="text-center">
                            <div className="font-display text-[15px] text-white">Drop a file here or click to browse</div>
                            <div className="mt-1 text-[12px] text-zinc-500 font-mono">.csv · .xlsx · .json · up to 100MB</div>
                        </div>
                        <input
                            id="analytics-file-input"
                            data-testid="analytics-file-input"
                            type="file"
                            className="sr-only"
                            onChange={(e) => onFile(e.target.files?.[0])}
                            accept=".csv,.xlsx,.xls,.json"
                        />
                    </label>

                    <div className="mt-4 flex items-center justify-between">
                        <button
                            data-testid="load-sample-btn"
                            onClick={loadSample}
                            className="text-[12px] text-indigo-300 hover:text-indigo-200 font-mono uppercase tracking-[0.2em]"
                        >
                            Load sample dataset →
                        </button>
                        {dataset && (
                            <button
                                data-testid="clear-dataset-btn"
                                onClick={() => { setDataset(null); setResults(null); }}
                                className="inline-flex items-center gap-1 text-[12px] text-zinc-400 hover:text-white"
                            >
                                <X className="w-3.5 h-3.5" /> Clear
                            </button>
                        )}
                    </div>

                    {dataset && (
                        <div className="mt-5 rounded-xl border border-white/10 bg-white/[0.02] p-4 animate-in-up">
                            <div className="flex items-center gap-3">
                                <FileSpreadsheet className="w-4 h-4 text-emerald-300" />
                                <div className="text-sm text-white truncate">{dataset.name}</div>
                                <Chip className="ml-auto text-emerald-300 border-emerald-500/20 bg-emerald-500/10">
                                    <CheckCircle2 className="w-3 h-3" />
                                    ready
                                </Chip>
                            </div>
                            <div className="mt-3 grid grid-cols-3 gap-3">
                                <StatChip label="Rows" value={dataset.rows.toLocaleString()} />
                                <StatChip label="Cols" value={dataset.cols} />
                                <StatChip label="Size" value={dataset.size} />
                            </div>
                        </div>
                    )}

                    <Button
                        data-testid="run-analysis-btn"
                        disabled={!dataset || running}
                        onClick={runAnalysis}
                        className="mt-5 w-full bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white border-0 shadow-[0_0_28px_rgba(79,70,229,0.35)] disabled:opacity-50"
                    >
                        {running ? <><Loader2 className="w-4 h-4 animate-spin" /> Running…</> : <><Play className="w-4 h-4" /> Run analysis</>}
                    </Button>
                </div>
            </Panel>

            {dataset && (
                <Panel className="animate-in-up">
                    <PanelHeader
                        eyebrow="Preview"
                        title="First rows"
                        description="Sampled directly from the dataset for quick sanity check."
                    />
                    <div className="px-6 pb-6 overflow-x-auto">
                        <Table>
                            <TableHeader>
                                <TableRow className="hover:bg-transparent border-white/5">
                                    {SAMPLE_DATASET.columns.slice(0, 6).map((c) => (
                                        <TableHead key={c} className="text-[10px] font-mono uppercase tracking-[0.2em] text-zinc-500">
                                            {c}
                                        </TableHead>
                                    ))}
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {SAMPLE_DATASET.preview.map((row, i) => (
                                    <TableRow key={i} className="border-white/5 hover:bg-white/[0.02]">
                                        {row.slice(0, 6).map((cell, j) => (
                                            <TableCell key={j} className="text-[13px] font-mono text-zinc-300">
                                                {String(cell)}
                                            </TableCell>
                                        ))}
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </Panel>
            )}
        </div>

        {/* RIGHT: results */}
        <div className="xl:col-span-7 space-y-6">
            <Panel className="animate-in-up min-h-[240px]">
                <PanelHeader
                    eyebrow="Step 02 · Results"
                    title="Analysis output"
                    description="Structured findings from the Analytics Agent — ready to feed Prediction and Insight."
                    actions={results ? <Chip className="text-emerald-300 border-emerald-500/20 bg-emerald-500/10"><CheckCircle2 className="w-3 h-3" />complete</Chip> : null}
                />
                <div className="px-6 pb-6">
                    {!results && !running && (
                        <div className="rounded-xl border border-dashed border-white/10 p-10 text-center">
                            <div className="font-display text-white text-lg">No results yet</div>
                            <p className="mt-1 text-sm text-zinc-500">Upload a dataset and press <span className="font-mono text-zinc-300">Run analysis</span> to profile it.</p>
                        </div>
                    )}
                    {running && (
                        <div className="rounded-xl border border-white/10 p-10 flex items-center gap-4">
                            <Loader2 className="w-5 h-5 animate-spin text-indigo-300" />
                            <div>
                                <div className="text-white text-sm">Analytics Agent is profiling your data…</div>
                                <div className="text-[12px] text-zinc-500 font-mono">tokenizing · profiling · clustering · anomaly detection</div>
                            </div>
                        </div>
                    )}
                    {results && (
                        <div className="space-y-6">
                            <p className="text-[15px] text-zinc-200 leading-relaxed border-l-2 border-indigo-500/60 pl-4">
                                {results.summary}
                            </p>

                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                {results.metrics.map((m) => (
                                    <StatChip key={m.label} label={m.label} value={m.value} />
                                ))}
                            </div>

                            <div>
                                <SectionLabel className="mb-3">Category distribution</SectionLabel>
                                <div className="space-y-2.5">
                                    {results.distribution.map((d) => (
                                        <div key={d.name} className="flex items-center gap-3">
                                            <div className="w-40 text-[13px] text-zinc-300">{d.name}</div>
                                            <div className="flex-1 h-2 rounded-full bg-white/[0.04] overflow-hidden">
                                                <div
                                                    className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400"
                                                    style={{ width: `${(d.value / maxDist) * 100}%` }}
                                                />
                                            </div>
                                            <div className="w-10 text-right text-[12px] font-mono text-zinc-400">{d.value}%</div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <SectionLabel className="mb-3">Detected anomalies</SectionLabel>
                                <div className="space-y-2">
                                    {results.anomalies.map((a, i) => (
                                        <div
                                            key={i}
                                            data-testid={`anomaly-${i}`}
                                            className={cn("flex gap-3 rounded-xl border p-3", SEVERITY_COLOR[a.severity])}
                                        >
                                            <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                                            <div className="min-w-0">
                                                <div className="text-[13px] font-medium">{a.where}</div>
                                                <div className="text-[12px] opacity-80">{a.detail}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </Panel>
        </div>
    </div>
);


export default AnalyticsWorkspace;
