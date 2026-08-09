type AIExplanation = {
  summary: string;
  detailed_explanation: string;
  action_plan: string[];
  provider_name: string;
  model_name: string;
  prompt_version: string;
};

type AIExplanationCardProps = {
  explanation?: AIExplanation | null;
  isLoading?: boolean;
  error?: string | null;
};

export function AIExplanationCard({
  explanation,
  isLoading = false,
  error = null,
}: AIExplanationCardProps) {
  if (isLoading) {
    return (
      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-3 text-lg font-semibold text-white">
          AI Explanation
        </h3>

        <div className="space-y-3">
          <div className="h-4 w-1/3 rounded bg-slate-800" />
          <div className="h-4 w-full rounded bg-slate-800" />
          <div className="h-4 w-5/6 rounded bg-slate-800" />
          <div className="h-4 w-2/3 rounded bg-slate-800" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-3 text-lg font-semibold text-white">
          AI Explanation
        </h3>

        <p className="text-slate-400">Unable to display AI explanation.</p>
      </div>
    );
  }

  if (!explanation) {
    return (
      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-3 text-lg font-semibold text-white">
          AI Explanation
        </h3>

        <p className="text-slate-400">No AI explanation available.</p>
      </div>
    );
  }

  const hasActionPlan = explanation.action_plan.length > 0;

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
      <h3 className="mb-4 text-lg font-semibold text-white">AI Explanation</h3>

      <div className="space-y-5">
        <div>
          <p className="text-xs uppercase text-slate-400">Summary</p>

          <p className="mt-1 text-slate-300">{explanation.summary}</p>
        </div>

        <div>
          <p className="text-xs uppercase text-slate-400">
            Detailed explanation
          </p>

          <p className="mt-1 whitespace-pre-wrap text-slate-300">
            {explanation.detailed_explanation}
          </p>
        </div>

        {hasActionPlan && (
          <div>
            <p className="text-xs uppercase text-slate-400">Action plan</p>

            <ul className="mt-2 space-y-1 text-slate-300">
              {explanation.action_plan.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
