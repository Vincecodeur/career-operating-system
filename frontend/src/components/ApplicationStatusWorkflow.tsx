type Props = {
  currentStatus: string;
  onStatusChange: (status: string) => void;
  disabled?: boolean;
};

const workflow = ["Applied", "Phone Screen", "Interview", "Offer", "Accepted"];

const validTransitions: Record<string, string[]> = {
  Applied: ["Phone Screen", "Rejected", "Withdrawn"],
  "Phone Screen": ["Interview", "Rejected", "Withdrawn"],
  Interview: ["Offer", "Rejected", "Withdrawn"],
  Offer: ["Accepted", "Rejected", "Withdrawn"],
  Accepted: [],
  Rejected: [],
  Withdrawn: [],
};

export function ApplicationStatusWorkflow({
  currentStatus,
  onStatusChange,
  disabled = false,
}: Props) {
  const availableTransitions = validTransitions[currentStatus] ?? [];

  return (
    <div className="space-y-4">
      <div className="space-y-3">
        {workflow.map((status) => (
          <div
            key={status}
            className={`rounded-md border p-3 ${
              status === currentStatus
                ? "border-blue-500 bg-blue-500/10"
                : "border-slate-700"
            }`}>
            <p className="font-medium text-white">{status}</p>
          </div>
        ))}
      </div>

      <div className="border-t border-slate-700 pt-4">
        <p className="mb-2 text-sm text-slate-400">Terminal statuses</p>

        <div className="flex gap-2">
          <span
            className={`rounded px-3 py-1 ${
              currentStatus === "Rejected"
                ? "bg-red-500/30 text-red-200"
                : "bg-red-500/20 text-red-300"
            }`}>
            Rejected
          </span>

          <span
            className={`rounded px-3 py-1 ${
              currentStatus === "Withdrawn"
                ? "bg-slate-500/30 text-slate-100"
                : "bg-slate-500/20 text-slate-300"
            }`}>
            Withdrawn
          </span>
        </div>
      </div>

      <div className="border-t border-slate-700 pt-4">
        <p className="mb-3 text-sm font-medium text-slate-300">
          Available actions
        </p>

        {availableTransitions.length === 0 ? (
          <p className="text-sm text-slate-400">
            No status transition available.
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {availableTransitions.map((status) => (
              <button
                key={status}
                type="button"
                disabled={disabled}
                onClick={() => onStatusChange(status)}
                className="rounded-md border border-blue-500 px-3 py-2 text-sm font-medium text-blue-300 transition hover:bg-blue-500/10 disabled:cursor-not-allowed disabled:opacity-50">
                Move to {status}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
