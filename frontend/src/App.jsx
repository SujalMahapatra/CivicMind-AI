import React, { useState } from "react";
import "@/App.css";
import { Sidebar } from "@/components/civic/Sidebar";
import { Header } from "@/components/civic/Header";
import OverviewWorkspace from "@/components/workspaces/OverviewWorkspace";
import AnalyticsWorkspace from "@/components/workspaces/AnalyticsWorkspace";
import PredictionWorkspace from "@/components/workspaces/PredictionWorkspace";
import InsightWorkspace from "@/components/workspaces/InsightWorkspace";
import RecommendationWorkspace from "@/components/workspaces/RecommendationWorkspace";
import KnowledgeWorkspace from "@/components/workspaces/KnowledgeWorkspace";
import ArchitectureWorkspace from "@/components/workspaces/ArchitectureWorkspace";
import { Toaster } from "@/components/ui/sonner";

function App() {
  const [active, setActive] = useState("overview");
  const [collapsed, setCollapsed] = useState(false);

  const gotoWorkspace = (key) => setActive(key);

  const renderWorkspace = () => {
    switch (active) {
      case "analytics":      return <AnalyticsWorkspace />;
      case "prediction":     return <PredictionWorkspace />;
      case "insight":        return <InsightWorkspace />;
      case "recommendation": return <RecommendationWorkspace />;
      case "knowledge":      return <KnowledgeWorkspace />;
      case "architecture":   return <ArchitectureWorkspace />;
      case "overview":
      default:               return <OverviewWorkspace onGoto={gotoWorkspace} />;
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground relative">
      {/* Ambient background */}
      <div className="aurora-bg" aria-hidden />
      <div className="grid-noise" aria-hidden />

      <div className="relative z-10 flex h-screen">
        <Sidebar
          active={active}
          onChange={setActive}
          collapsed={collapsed}
          onToggle={() => setCollapsed((c) => !c)}
        />

        <div className="flex-1 min-w-0 flex flex-col">
          <Header active={active} />
          <main
            data-testid={`workspace-${active}`}
            className="flex-1 overflow-y-auto"
          >
            <div className="mx-auto max-w-[1440px] px-6 md:px-8 py-8">
              <div key={active} className="animate-in-up">
                {renderWorkspace()}
              </div>
            </div>
          </main>
        </div>
      </div>

      <Toaster theme="dark" position="bottom-right" />
    </div>
  );
}

export default App;
