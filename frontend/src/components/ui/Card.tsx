import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export function Card({ children }: Props) {
  return (
    <div className="rounded-lg border border-slate-700 bg-slate-900 p-6">
      {children}
    </div>
  );
}
