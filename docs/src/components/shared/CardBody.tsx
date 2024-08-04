import type { ReactNode } from "react";

export default function CardBody({ children }: { children: ReactNode }) {
  return (
    <div className="rounded-b-xl border border-slate-600 border-solid">{children}</div>
  );
}
