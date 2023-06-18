import { ReactNode } from "react";

export default function CardHeader({ children }: { children: ReactNode }) {
  return (
    <div className="rounded-t-xl border border-solid border-slate-700 bg-slate-950 p-4 text-xl">
      {children}
    </div>
  );
}
