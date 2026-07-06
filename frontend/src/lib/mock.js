/**
 * CivicMind AI Demo Data
 *
 * Purpose:
 * Temporary mock data used during frontend development.
 *
 * Future:
 * Replace with FastAPI responses from:
 * - Analytics Agent
 * - Prediction Agent
 * - Insight Agent
 * - Recommendation Agent
 * - RAG Agent
 */
// Mock data for CivicMind AI dashboard.
// Structured so real API responses can drop in without UI changes.

import {
  Bot, LineChart, Brain, Lightbulb, ListChecks, MessagesSquare,
} from "lucide-react";

export const AGENTS = [
  {
    id: "coordinator",
    name: "Coordinator Agent",
    role: "Orchestrator",
    description: "Routes decisions across specialized agents in real time.",
    status: "active",
    latency: "42ms",
    calls: 1284,
    accent: "from-indigo-500 to-blue-500",
    icon: Bot,
    featured: true,
  },
  {
    id: "analytics",
    name: "Analytics Agent",
    role: "Data Understanding",
    description: "Profiles civic datasets, detects patterns and anomalies.",
    status: "active",
    latency: "128ms",
    calls: 842,
    accent: "from-sky-500 to-cyan-500",
    icon: LineChart,
  },
  {
    id: "prediction",
    name: "Prediction Agent",
    role: "Forecasting",
    description: "Time-series forecasts for demand, load, and outcomes.",
    status: "active",
    latency: "260ms",
    calls: 611,
    accent: "from-blue-500 to-indigo-500",
    icon: Brain,
  },
  {
    id: "insight",
    name: "Insight Agent",
    role: "Narrative Reasoning",
    description: "Synthesizes findings into human-readable insights.",
    status: "idle",
    latency: "—",
    calls: 407,
    accent: "from-violet-500 to-fuchsia-500",
    icon: Lightbulb,
  },
  {
    id: "recommendation",
    name: "Recommendation Agent",
    role: "Actions",
    description: "Suggests prioritized civic interventions and next-best-actions.",
    status: "active",
    latency: "184ms",
    calls: 293,
    accent: "from-emerald-500 to-teal-500",
    icon: ListChecks,
  },
  {
    id: "rag",
    name: "RAG Knowledge Assistant",
    role: "Retrieval + Reasoning",
    description: "Answers grounded in indexed civic policies and reports.",
    status: "active",
    latency: "310ms",
    calls: 1120,
    accent: "from-cyan-500 to-blue-500",
    icon: MessagesSquare,
  },
];

export const TECH_STACK = [
  {
    name: "FastAPI",
    tag: "Backend API",
    color: "text-green-400"
  },
  {
    name: "Gemini 2.5",
    tag: "LLM Engine",
    color: "text-blue-400"
  },
  {
    name: "ChromaDB",
    tag: "Vector Store",
    color: "text-purple-400"
  },
  {
    name: "React",
    tag: "Frontend",
    color: "text-cyan-400"
  },
  {
    name: "Scikit-Learn",
    tag: "Forecasting",
    color: "text-orange-400"
  }
];

export const SAMPLE_DATASET = {
  name: "city_service_requests_2024.csv",
  rows: 12480,
  cols: 8,
  size: "1.9 MB",
  columns: ["ticket_id", "district", "category", "priority", "reported_at", "resolved_at", "resolution_hours", "satisfaction"],
  preview: [
    ["CS-10241", "North", "Sanitation", "High", "2024-01-04", "2024-01-05", 26.4, 4.1],
    ["CS-10242", "Central", "Roads & Traffic", "Medium", "2024-01-04", "2024-01-06", 44.1, 3.6],
    ["CS-10243", "East", "Water Supply", "High", "2024-01-05", "2024-01-05", 8.2, 4.8],
    ["CS-10244", "South", "Street Lighting", "Low", "2024-01-05", "2024-01-09", 96.7, 3.1],
    ["CS-10245", "North", "Sanitation", "High", "2024-01-06", "2024-01-07", 22.9, 4.4],
    ["CS-10246", "West", "Parks", "Low", "2024-01-06", "2024-01-11", 118.3, 3.0],
  ],
};

export const ANALYSIS_RESULTS = {
  summary: "Analytics agent profiled 12,480 records across 8 fields. Sanitation dominates volume (34%), while Street Lighting shows the worst SLA breach rate (41%). Overall satisfaction is 3.8 / 5 with clear district-level disparities.",
  metrics: [
    { label: "Records analyzed", value: "12,480" },
    { label: "Median resolution", value: "26.4h" },
    { label: "SLA breach rate", value: "18.2%" },
    { label: "Avg. satisfaction", value: "3.8 / 5" },
  ],
  distribution: [
    { name: "Sanitation", value: 34 },
    { name: "Roads & Traffic", value: 22 },
    { name: "Street Lighting", value: 14 },
    { name: "Water Supply", value: 12 },
    { name: "Parks", value: 9 },
    { name: "Other", value: 9 },
  ],
  anomalies: [
    { where: "South district — Street Lighting", detail: "SLA breach rate 3.1× the citywide average.", severity: "high" },
    { where: "West district — Parks", detail: "Median resolution 118h — outlier vs 26h median.", severity: "medium" },
    { where: "Central — Roads & Traffic", detail: "Volume spike +38% over trailing 30 days.", severity: "medium" },
  ],
};

export const PREDICTION_RESULT = {
  target: "resolution_hours",
  horizon: 14,
  trend: "Slight upward drift (+4.6%) over the next two weeks, driven by seasonal sanitation demand.",
  forecast: Array.from({ length: 14 }, (_, i) => ({
    day: `D+${i + 1}`,
    value: +(26 + Math.sin(i / 2) * 3 + i * 0.35).toFixed(2),
    lower: +(24 + Math.sin(i / 2) * 2.5 + i * 0.25).toFixed(2),
    upper: +(28 + Math.sin(i / 2) * 3.5 + i * 0.45).toFixed(2),
  })),
  confidence: 0.86,
};

export const INSIGHT_TEXT = `Sanitation is now the single largest driver of citizen dissatisfaction across the North and Central districts, accounting for 34% of tickets and 41% of SLA breaches over the last quarter.

Street Lighting failures in the South district cluster around three specific wards where resolution consistently exceeds 96 hours — 3.1× the citywide average. This pattern strongly correlates with reduced pedestrian activity at night, and — based on cross-referenced safety data — a measurable rise in incident reports.

The Prediction Agent forecasts a +4.6% drift in resolution times over the next 14 days, primarily driven by seasonal sanitation load. Left unaddressed, satisfaction is projected to decline from 3.8 to ~3.5 by end of month.

Recommended focus: reroute one sanitation crew to North + Central, and initiate a targeted Street Lighting audit in South wards 7, 9, and 12.`;

export const RECOMMENDATIONS = [
  {
    id: "r1",
    title: "Reallocate sanitation crew to North + Central",
    category: "Operations",
    impact: "High",
    effort: "Low",
    timeframe: "This week",
    description: "Shifting 1 crew from West (surplus capacity) closes the 41% SLA gap in the two highest-volume districts.",
    expectedOutcome: "SLA breach ↓ 22%",
  },
  {
    id: "r2",
    title: "Audit Street Lighting in South wards 7, 9, 12",
    category: "Infrastructure",
    impact: "High",
    effort: "Medium",
    timeframe: "2 weeks",
    description: "Cluster of chronic 96h+ resolution times. Field survey + circuit inspection recommended.",
    expectedOutcome: "Ward resolution median ↓ 60%",
  },
  {
    id: "r3",
    title: "Publish district-level SLA dashboard",
    category: "Transparency",
    impact: "Medium",
    effort: "Low",
    timeframe: "3 days",
    description: "Public visibility reduces repeat tickets and increases perceived responsiveness (avg. +0.4 CSAT in comparable cities).",
    expectedOutcome: "Satisfaction ↑ 0.3",
  },
  {
    id: "r4",
    title: "Predictive routing for Roads & Traffic tickets",
    category: "Automation",
    impact: "Medium",
    effort: "Medium",
    timeframe: "1 month",
    description: "Route high-priority tickets to specialized crews based on forecasted volume windows.",
    expectedOutcome: "Median resolution ↓ 18%",
  },
];

export const ACTION_CATEGORIES = [
  { key: "Operations", color: "text-indigo-300", bg: "bg-indigo-500/10", ring: "ring-indigo-500/30" },
  { key: "Infrastructure", color: "text-cyan-300", bg: "bg-cyan-500/10", ring: "ring-cyan-500/30" },
  { key: "Transparency", color: "text-emerald-300", bg: "bg-emerald-500/10", ring: "ring-emerald-500/30" },
  { key: "Automation", color: "text-violet-300", bg: "bg-violet-500/10", ring: "ring-violet-500/30" },
];

export const KNOWLEDGE_SUGGESTIONS = [
  "What are the top 3 civic priorities this month?",
  "Summarize the sanitation SLA policy for North district.",
  "Which wards had the worst street lighting outcomes?",
  "Compare our resolution times to peer cities.",
];

// Simulated grounded RAG answer for demo purposes.
export function mockKnowledgeAnswer(question) {
  const q = (question || "").toLowerCase();
  if (q.includes("priorit")) {
    return {
      answer:
        "Based on indexed civic reports and last quarter's ticket data, the top three priorities are: (1) closing the sanitation SLA gap in North and Central districts, (2) resolving chronic street-lighting failures in South wards 7, 9, and 12, and (3) publishing a district-level SLA dashboard to reduce repeat tickets. These are ranked by projected impact on citizen satisfaction and by breach severity.",
      sources: [
        { title: "Q4 Civic Service Report", page: 14, ref: "civic-q4.pdf#p14" },
        { title: "SLA Policy — Master Document", page: 3, ref: "sla-policy.md#sec-3" },
        { title: "District Comparative Study", page: 22, ref: "district-study.pdf#p22" },
      ],
    };
  }
  if (q.includes("sanitation") || q.includes("sla")) {
    return {
      answer:
        "The Sanitation SLA for the North district mandates first response within 12 hours and full resolution within 36 hours for High-priority tickets. Current performance shows a median resolution of 22.9 hours (within SLA) but a breach rate of 41% concentrated in two collection zones. The policy also requires weekly reporting to the district commissioner.",
      sources: [
        { title: "SLA Policy — Sanitation Annex", page: 7, ref: "sla-policy.md#sanitation" },
        { title: "North District Ops Handbook", page: 12, ref: "north-ops.pdf#p12" },
      ],
    };
  }
  if (q.includes("light")) {
    return {
      answer:
        "Street lighting outcomes are worst in South wards 7, 9, and 12, where median resolution consistently exceeds 96 hours — 3.1× the citywide average. Root-cause analysis in the Q3 Infrastructure Report attributes this to aging circuit infrastructure and a single overloaded field team.",
      sources: [
        { title: "Q3 Infrastructure Report", page: 9, ref: "infra-q3.pdf#p9" },
        { title: "Field Ops Load Analysis", page: 4, ref: "field-load.md#p4" },
      ],
    };
  }
  if (q.includes("compare") || q.includes("peer")) {
    return {
      answer:
        "Compared to peer cities of similar population size, our median resolution time (26.4h) is 12% better, but our SLA breach rate (18.2%) is 4 points worse — indicating good average performance but poor tail-risk handling. Peer cities that published public SLA dashboards saw an average +0.4 CSAT lift within six months.",
      sources: [
        { title: "Peer City Benchmark 2024", page: 6, ref: "benchmark.pdf#p6" },
        { title: "Transparency & CSAT Meta-study", page: 18, ref: "meta-study.pdf#p18" },
      ],
    };
  }
  return {
    answer:
      "I've searched the indexed civic knowledge base for that question. Based on the most relevant documents, the CivicMind agents recommend cross-referencing the latest Analytics run and the SLA Policy master document. Ask me anything more specific about districts, categories, SLAs, or forecasts and I'll ground my answer in citations.",
    sources: [
      { title: "Civic Knowledge Base — Index", page: 1, ref: "kb-index.md" },
      { title: "SLA Policy — Master Document", page: 1, ref: "sla-policy.md#p1" },
    ],
  };
}
