import React from "react";

export function Table({ children, className = "" }) {
  return (
    <div className="overflow-x-auto">
      <table className={`w-full ${className}`}>
        {children}
      </table>
    </div>
  );
}

export function TableHeader({ children, className = "" }) {
  return <thead className={className}>{children}</thead>;
}

export function TableBody({ children, className = "" }) {
  return <tbody className={className}>{children}</tbody>;
}

export function TableRow({ children, className = "" }) {
  return <tr className={className}>{children}</tr>;
}

export function TableHead({ children, className = "" }) {
  return (
    <th
      className={`px-4 py-2 text-left font-medium text-zinc-300 ${className}`}
    >
      {children}
    </th>
  );
}

export function TableCell({ children, className = "" }) {
  return (
    <td className={`px-4 py-2 text-zinc-200 ${className}`}>
      {children}
    </td>
  );
}