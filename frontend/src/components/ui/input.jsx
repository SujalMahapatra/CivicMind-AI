import React from "react";

export function Input({
  className = "",
  ...props
}) {
  return (
    <input
      className={`
        w-full
        rounded-lg
        border border-white/10
        bg-white/[0.03]
        px-3 py-2
        text-white
        outline-none
        focus:border-indigo-500
        ${className}
      `}
      {...props}
    />
  );
}