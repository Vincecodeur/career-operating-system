import type { ReactNode } from "react";

import { Card } from "./Card";

type Props = {
  title: string;
  children: ReactNode;
};

export function Section({ title, children }: Props) {
  return (
    <section className="mb-10">
      <h2 className="mb-4 text-2xl font-semibold text-white">{title}</h2>

      <Card>{children}</Card>
    </section>
  );
}
