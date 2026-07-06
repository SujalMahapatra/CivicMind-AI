import React from "react";

export function Button({
  children,
  className = "",
  variant = "default",
  size = "default",
  ...props
}) {
  return (
    <button
      className={className}
      {...props}
    >
      {children}
    </button>
  );
}