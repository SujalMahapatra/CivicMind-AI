
import React from "react";
import { cn } from "@/lib/utils";

// Glassmorphism / bordered surface used across the dashboard.
export const Panel = React.forwardRef(({ className, beam = false, children, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "relative rounded-2xl",
      "bg-[#0A0A12]/70 backdrop-blur-xl border border-white/[0.06]",
      "shadow-[0_1px_0_0_rgba(255,255,255,0.03)_inset,0_20px_60px_-30px_rgba(0,0,0,0.8)]",
      beam && "beam",
      className
    )}
    {...props}
  >
    {children}
  </div>
));
Panel.displayName = "Panel";

export const PanelHeader = ({ eyebrow, title, description, actions, className }) => (
  <div className={cn("flex items-start justify-between gap-6 p-6 pb-4", className)}>
    <div className="min-w-0">
      {eyebrow && (
        <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-indigo-300/80 mb-2">
          {eyebrow}
        </div>
      )}
      <h3 className="font-display text-lg font-medium text-white tracking-tight">{title}</h3>
      {description && <p className="mt-1 text-sm text-zinc-400 leading-relaxed">{description}</p>}
    </div>
    {actions && <div className="shrink-0 flex items-center gap-2">{actions}</div>}
  </div>
);

export const StatChip = ({ label, value, hint }) => (
  <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4">
    <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500">{label}</div>
    <div className="mt-1.5 font-display text-2xl text-white tracking-tight">{value}</div>
    {hint && <div className="mt-1 text-[11px] text-zinc-500">{hint}</div>}
  </div>
);

export const SectionLabel = ({ children, className }) => (
  <div className={cn("text-[10px] font-mono uppercase tracking-[0.25em] text-zinc-500", className)}>
    {children}
  </div>
);

export const StatusDot = ({ status = "active" }) => {
  const cls = status === "active" ? "" : status === "idle" ? "idle" : "error";
  return <span className={cn("pulse-dot", cls)} aria-label={`status-${status}`} />;
};

export const Chip = ({ children, className, ...props }) => (
  <span
    className={cn(
      "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-medium",
      "bg-white/[0.04] border border-white/10 text-zinc-300",
      className
    )}
    {...props}
  >
    {children}
  </span>
);
