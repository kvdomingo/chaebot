import { ReactNode } from "react";

export default function CardBody({ children }: { children: ReactNode }) {
  return (
    <div className="rounded-b-xl border border-solid border-slate-600">
      {children}
    </div>
  );
}
