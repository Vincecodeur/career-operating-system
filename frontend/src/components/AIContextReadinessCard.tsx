import type { AIContextPreview } from "../services/api";
import { Card } from "./ui/Card";

type Props = {
  aiContextPreview: AIContextPreview | null;
};

export function AIContextReadinessCard({ aiContextPreview }: Props) {
  if (!aiContextPreview) {
    return (
      <Card>
        <h3 className="mb-2 text-lg font-semibold text-white">
          AI Context Readiness
        </h3>

        <p className="text-slate-400">AI context preview unavailable.</p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-white">
            AI Context Readiness
          </h3>

          <p className="mt-1 text-sm text-slate-400">
            Backend-controlled AI readiness evaluation.
          </p>
        </div>

        <div
          className={
            aiContextPreview.is_ai_ready
              ? "rounded-full bg-green-500/10 px-3 py-1 text-sm font-medium text-green-300"
              : "rounded-full bg-red-500/10 px-3 py-1 text-sm font-medium text-red-300"
          }>
          {aiContextPreview.is_ai_ready ? "AI Ready" : "Not Ready"}
        </div>
      </div>

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">AI Features</p>

          <p className="mt-2 text-xl font-semibold text-white">
            {aiContextPreview.ai_features_enabled ? "Enabled" : "Disabled"}
          </p>
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">Consent</p>

          <p className="mt-2 text-xl font-semibold text-white">
            {aiContextPreview.ai_consent_accepted ? "Accepted" : "Not Accepted"}
          </p>
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">AI Call</p>

          <p className="mt-2 text-xl font-semibold text-white">
            {aiContextPreview.ai_call_allowed ? "Allowed" : "Blocked"}
          </p>
        </div>
      </div>

      <div className="mb-6">
        <h4 className="mb-2 font-medium text-white">Available Categories</h4>

        <div className="flex flex-wrap gap-2">
          {aiContextPreview.available_categories.map((category) => (
            <span
              key={category}
              className="rounded-full border border-blue-700 bg-blue-950 px-3 py-1 text-sm text-blue-300">
              {category}
            </span>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <h4 className="mb-2 font-medium text-white">
          Missing Required Information
        </h4>

        {aiContextPreview.missing_required_information.length === 0 ? (
          <p className="text-green-400">No required information missing.</p>
        ) : (
          <ul className="space-y-1 text-slate-300">
            {aiContextPreview.missing_required_information.map((value) => (
              <li key={value}>• {value}</li>
            ))}
          </ul>
        )}
      </div>

      <div className="mb-6">
        <h4 className="mb-2 font-medium text-white">
          Missing Optional Categories
        </h4>

        {aiContextPreview.missing_optional_categories.length === 0 ? (
          <p className="text-green-400">No optional category missing.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {aiContextPreview.missing_optional_categories.map((category) => (
              <span
                key={category}
                className="rounded-full border border-yellow-700 bg-yellow-950 px-3 py-1 text-sm text-yellow-300">
                {category}
              </span>
            ))}
          </div>
        )}
      </div>

      <div>
        <h4 className="mb-2 font-medium text-white">Excluded Categories</h4>

        <div className="flex flex-wrap gap-2">
          {aiContextPreview.excluded_categories.map((category) => (
            <span
              key={category}
              className="rounded-full border border-red-700 bg-red-950 px-3 py-1 text-sm text-red-300">
              {category}
            </span>
          ))}
        </div>
      </div>
    </Card>
  );
}
