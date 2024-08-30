import type { AnchorHTMLAttributes, DetailedHTMLProps } from "react";

import { cn } from "@/utils";

interface ButtonLinkProps
  extends DetailedHTMLProps<
    AnchorHTMLAttributes<HTMLAnchorElement>,
    HTMLAnchorElement
  > {
  disabled?: boolean;
}

export default function ButtonLink({
  className,
  children,
  disabled = false,
  ...props
}: ButtonLinkProps) {
  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      className={cn(
        "rounded border border-solid px-4 py-1 active:brightness-125",
        "transition-all duration-100 ease-in-out hover:text-slate-800",
        className,
        {
          "pointer-events-none border-gray-500 text-gray-500": disabled,
        },
      )}
      {...props}
    >
      {children}
    </a>
  );
}
