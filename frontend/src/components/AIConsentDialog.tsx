type Props = {
  isOpen: boolean;
  isSaving: boolean;
  onAccept: () => void;
  onCancel: () => void;
};

export function AIConsentDialog({
  isOpen,
  isSaving,
  onAccept,
  onCancel,
}: Props) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white">Enable AI Features</h2>

        <p className="mt-3 text-slate-300">
          Future AI features may use validated profile data to provide guidance
          and recommendations.
        </p>

        <div className="mt-6 rounded-lg border border-slate-700 bg-slate-950 p-4">
          <h3 className="mb-3 font-semibold text-white">
            Data That May Be Used
          </h3>

          <ul className="space-y-1 text-slate-300">
            <li>• Profile information</li>
            <li>• Career goals</li>
            <li>• Hard skills</li>
            <li>• Soft skills</li>
            <li>• Languages</li>
            <li>• Certifications</li>
            <li>• Work experiences</li>
            <li>• Additional profile context</li>
          </ul>
        </div>

        <div className="mt-4 rounded-lg border border-red-800 bg-red-950 p-4">
          <h3 className="mb-3 font-semibold text-red-300">
            Explicitly Excluded
          </h3>

          <ul className="space-y-1 text-red-200">
            <li>• Raw CV files</li>
            <li>• Extracted CV text</li>
            <li>• Unvalidated enrichment proposals</li>
            <li>• Application history</li>
            <li>• Technical secrets</li>
          </ul>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={onCancel}
            disabled={isSaving}
            className="rounded-md border border-slate-600 px-4 py-2 text-slate-300 hover:bg-slate-800">
            Cancel
          </button>

          <button
            type="button"
            onClick={onAccept}
            disabled={isSaving}
            className="rounded-md bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500">
            {isSaving ? "Saving..." : "Accept and Enable AI"}
          </button>
        </div>
      </div>
    </div>
  );
}
