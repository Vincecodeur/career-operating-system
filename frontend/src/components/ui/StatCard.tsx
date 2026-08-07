type Props = {
  title: string;
  value: string | number;
};

export function StatCard({ title, value }: Props) {
  return (
    <div className="rounded-lg border border-slate-700 bg-slate-900 p-6">
      <p className="text-sm text-slate-400">{title}</p>

      <p className="mt-2 text-3xl font-bold text-white">{value}</p>
    </div>
  );
}
