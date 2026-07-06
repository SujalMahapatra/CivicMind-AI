export function Select({
  children,
  value,
  onValueChange,
  className = ""
}) {
  return (
    <select
      className={`
        w-full rounded-lg
        border border-white/10
        bg-white/[0.03]
        px-3 py-2
        text-white
        ${className}
      `}
      value={value}
      onChange={(e) => onValueChange?.(e.target.value)}
    >
      {children}
    </select>
  );
}

export function SelectItem({
  children,
  value
}) {
  return (
    <option value={value}>
      {children}
    </option>
  );
}

export function SelectTrigger({ children }) {
  return children;
}

export function SelectValue() {
  return null;
}

export function SelectContent({ children }) {
  return children;
}