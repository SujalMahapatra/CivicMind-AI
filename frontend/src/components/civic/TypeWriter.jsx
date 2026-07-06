import React, { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

/**
 * Types text out progressively. `key` prop of parent should change to restart.
 */
export const TypeWriter = ({ text = "", speed = 12, className, onDone }) => {
  const [out, setOut] = useState("");
  const [done, setDone] = useState(false);
  const idxRef = useRef(0);

  useEffect(() => {
    setOut("");
    setDone(false);
    idxRef.current = 0;
    if (!text) return;
    const id = setInterval(() => {
      idxRef.current += 1;
      setOut(text.slice(0, idxRef.current));
      if (idxRef.current >= text.length) {
        clearInterval(id);
        setDone(true);
        onDone && onDone();
      }
    }, speed);
    return () => clearInterval(id);
  }, [text, speed, onDone]);

  return (
    <div className={cn("whitespace-pre-wrap text-[15px] leading-[1.75] text-zinc-200", className)}>
      {out}
      {!done && <span className="caret" />}
    </div>
  );
};

export default TypeWriter;
