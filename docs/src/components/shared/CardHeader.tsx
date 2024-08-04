import type { ReactNode } from "react";

export default function CardHeader({ children }: { children: ReactNode }) {
  return (
    <div className="rounded-t-xl border border-slate-700 border-solid bg-slate-950 p-4 text-xl">
      {children}
    </div>
  );
}
