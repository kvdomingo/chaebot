import { ReactNode } from "react";

export default function Card({
  children,
  id,
}: {
  id?: string;
  children: ReactNode;
}) {
  return (
    <div id={id} className="my-6">
      {children}
    </div>
  );
}
