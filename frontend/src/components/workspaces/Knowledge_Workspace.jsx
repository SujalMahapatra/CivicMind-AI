import React, { useEffect, useRef, useState } from "react";
import { Panel, PanelHeader, SectionLabel, Chip } from "../civic/Primitives";
import { Send, User, Bot, Sparkles, Loader2, BookOpen } from "lucide-react";
import { cn } from "@/lib/utils";
import api from "@/services/api";

const KNOWLEDGE_SUGGESTIONS = [
    "What AQI level is considered unhealthy?",
    "What are WHO air quality guidelines?",
    "How can cities reduce air pollution?",
    "What health risks are associated with poor air quality?",
    "What actions should be taken during high AQI events?"
];
// Simple typewriter for streaming effect
function useStream(text, active) {
    const [out, setOut] = useState("");
    useEffect(() => {
        if (!active || !text) return;
        setOut("");
        let i = 0;
        const id = setInterval(() => {
            i += 3;
            setOut(text.slice(0, i));
            if (i >= text.length) clearInterval(id);
        }, 18);
        return () => clearInterval(id);
    }, [text, active]);
    return out;
}

const StreamingBubble = ({ text }) => {
    const shown = useStream(text, true);
    const done = shown.length >= (text?.length || 0);
    return (
        <div className="whitespace-pre-wrap text-[14px] leading-[1.65] text-zinc-100">
            {shown}
            {!done && <span className="caret" />}
        </div>
    );
};

export const KnowledgeWorkspace = () => {
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content: `Hi — I'm the CivicMind Knowledge Assistant.

                    Ask questions about:
                    • Air Quality
                    • Public Health
                    • Urban Mobility
                    • Environmental Policies
                    • Community Intelligence

                    All responses are grounded using the CivicMind knowledge base.`,
            sources: [{ title: "Welcome · CivicMind KB", ref: "welcome.md" }],
            streaming: false,
        },
    ]);
    const [q, setQ] = useState("");
    const [thinking, setThinking] = useState(false);
    const listRef = useRef(null);

    useEffect(() => {
        listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
    }, [messages, thinking]);

    const send = async (text) => {
        const question = (text ?? q).trim();

        if (!question) return;

        setMessages((m) => [
            ...m,
            {
                role: "user",
                content: question
            }
        ]);

        setQ("");
        setThinking(true);

        try {
            const response = await api.post(
                "/rag/ask",
                {
                    question
                }
            );

            setMessages((m) => [
                ...m,
                {
                    role: "assistant",
                    content: response.data.answer,
                    sources: [
                        {
                            title: response.data.source,
                            ref: response.data.source
                        }
                    ],
                    streaming: true
                }
            ]);

        } catch (error) {

            console.error(
                "RAG request failed",
                error
            );

            setMessages((m) => [
                ...m,
                {
                    role: "assistant",
                    content:
                        "Unable to retrieve an answer from the knowledge base.",
                    sources: [],
                    streaming: false
                }
            ]);

        } finally {
            setThinking(false);
        }
    };
    const onKey = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            send();
        }
    };

    return (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
            {/* CHAT */}
            <div className="xl:col-span-8">
                <Panel className="flex flex-col h-[calc(100vh-11rem)] min-h-[560px] animate-in-up">
                    <div className="px-6 pt-5 pb-4 border-b border-white/[0.06] flex items-center justify-between">
                        <div>
                            <SectionLabel>RAG Knowledge Assistant</SectionLabel>
                            <h3 className="mt-1 font-display text-lg text-white tracking-tight">Ask anything</h3>
                        </div>
                        <Chip className="text-cyan-300 border-cyan-500/20 bg-cyan-500/10">
                            <BookOpen className="w-3 h-3" />
                            1,204 docs indexed
                        </Chip>
                    </div>

                    {/* messages */}
                    <div
                        ref={listRef}
                        data-testid="chat-messages"
                        className="flex-1 overflow-y-auto px-6 py-6 space-y-5"
                    >
                        {messages.map((msg, i) => (
                            <div
                                key={i}
                                className={cn("flex gap-3", msg.role === "user" ? "justify-end" : "justify-start")}
                            >
                                {msg.role === "assistant" && (
                                    <div className="w-8 h-8 shrink-0 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 grid place-items-center">
                                        <Bot className="w-4 h-4 text-white" strokeWidth={1.6} />
                                    </div>
                                )}
                                <div
                                    className={cn(
                                        "max-w-[80%] rounded-2xl px-4 py-3 border",
                                        msg.role === "user"
                                            ? "bg-white/[0.06] border-white/10 text-white"
                                            : "bg-indigo-500/10 border-indigo-500/20 text-white"
                                    )}
                                >
                                    {msg.streaming
                                        ? <StreamingBubble text={msg.content} />
                                        : <div className="whitespace-pre-wrap text-[14px] leading-[1.65]">{msg.content}</div>}

                                    {msg.role === "assistant" && msg.sources && (
                                        <div className="mt-3 pt-3 border-t border-white/10 flex flex-wrap gap-1.5">
                                            <SectionLabel className="w-full mb-1">Sources</SectionLabel>
                                            {msg.sources.map((s, j) => (
                                                <span
                                                    key={j}
                                                    data-testid={`source-${i}-${j}`}
                                                    className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-mono bg-white/[0.04] border border-white/10 text-zinc-300 hover:text-white hover:border-white/20 transition-colors"
                                                    title={s.ref}
                                                >
                                                    <BookOpen className="w-3 h-3 text-cyan-300" />
                                                    {s.title}
                                                    {s.page && <span className="text-zinc-500">· p{s.page}</span>}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                {msg.role === "user" && (
                                    <div className="w-8 h-8 shrink-0 rounded-lg bg-white/[0.06] border border-white/10 grid place-items-center">
                                        <User className="w-4 h-4 text-zinc-200" strokeWidth={1.6} />
                                    </div>
                                )}
                            </div>
                        ))}

                        {thinking && (
                            <div className="flex gap-3">
                                <div className="w-8 h-8 shrink-0 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 grid place-items-center">
                                    <Bot className="w-4 h-4 text-white" strokeWidth={1.6} />
                                </div>
                                <div className="rounded-2xl px-4 py-3 bg-indigo-500/10 border border-indigo-500/20 text-zinc-300 text-[13px] flex items-center gap-2">
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                    retrieving & grounding…
                                </div>
                            </div>
                        )}
                    </div>

                    {/* input */}
                    <div className="px-6 py-4 border-t border-white/[0.06]">
                        <div className="flex items-end gap-2 rounded-xl border border-white/10 bg-white/[0.03] focus-within:border-indigo-500/50 focus-within:ring-2 focus-within:ring-indigo-500/20 px-3 py-2 transition-colors">
                            <Sparkles className="w-4 h-4 text-indigo-300 mt-1.5 shrink-0" />
                            <textarea
                                data-testid="chat-input"
                                value={q}
                                onChange={(e) => setQ(e.target.value)}
                                onKeyDown={onKey}
                                rows={1}
                                placeholder="Ask about SLAs, districts, forecasts, priorities…"
                                className="flex-1 bg-transparent outline-none resize-none text-[14px] text-white placeholder:text-zinc-500 py-1 max-h-32"
                            />
                            <button
                                data-testid="chat-send-btn"
                                onClick={() => send()}
                                disabled={!q.trim() || thinking}
                                className="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-[13px] font-medium bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white disabled:opacity-40 shadow-[0_0_20px_rgba(79,70,229,0.35)]"
                            >
                                Send <Send className="w-3.5 h-3.5" />
                            </button>
                        </div>
                        <p className="mt-2 text-[11px] text-zinc-500 font-mono">
                            Enter to send · Shift+Enter for newline · answers cite indexed sources
                        </p>
                    </div>
                </Panel>
            </div>

            {/* SUGGESTIONS + INDEX INFO */}
            <div className="xl:col-span-4 space-y-6">
                <Panel className="animate-in-up">
                    <PanelHeader eyebrow="Try asking" title="Suggested questions" />
                    <div className="px-6 pb-6 space-y-2">
                        {KNOWLEDGE_SUGGESTIONS.map((s, i) => (
                            <button
                                key={i}
                                data-testid={`suggestion-${i}`}
                                onClick={() => send(s)}
                                className="w-full text-left rounded-xl border border-white/10 bg-white/[0.02] hover:border-indigo-500/30 hover:bg-white/[0.04] transition-colors px-4 py-3 text-[13px] text-zinc-200 leading-snug"
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                </Panel>

                <Panel className="animate-in-up">
                    <PanelHeader eyebrow="Retrieval" title="Knowledge index" />
                    <div className="px-6 pb-6 space-y-3">
                        {[
                            { k: "Documents", v: "1,204" },
                            { k: "Chunks", v: "18,942" },
                            { k: "Embedding", v: "MiniLM-L6-v2" },
                            { k: "Vector DB", v: "ChromaDB" },
                        ].map((row) => (
                            <div key={row.k} className="flex items-center justify-between text-[13px] py-1.5 border-b border-white/[0.04] last:border-b-0">
                                <span className="text-zinc-500 font-mono">{row.k}</span>
                                <span className="text-white font-mono">{row.v}</span>
                            </div>
                        ))}
                    </div>
                </Panel>
            </div>
        </div>
    );
};

export default KnowledgeWorkspace;
