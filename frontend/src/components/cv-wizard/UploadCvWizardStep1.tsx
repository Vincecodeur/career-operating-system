type Props = {
  selectedFile: File | null;
  language: string;
  versionLabel: string;
  isDefault: boolean;
  isSaving: boolean;
  onFileChange: (file: File | null) => void;
  onLanguageChange: (value: string) => void;
  onVersionLabelChange: (value: string) => void;
  onIsDefaultChange: (value: boolean) => void;
};

export function UploadCvWizardStep1({
  selectedFile,
  language,
  versionLabel,
  isDefault,
  isSaving,
  onFileChange,
  onLanguageChange,
  onVersionLabelChange,
  onIsDefaultChange,
}: Props) {
  return (
    <div className="space-y-5">
      <div>
        <h3 className="text-lg font-semibold text-white">Step 1 - Upload CV</h3>

        <p className="mt-1 text-sm text-slate-400">
          Select the CV that will be used to update the profile.
        </p>
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-300">
          CV File
        </label>

        <input
          type="file"
          accept=".pdf,.doc,.docx"
          disabled={isSaving}
          onChange={(event) => {
            const file = event.target.files?.[0] ?? null;

            onFileChange(file);
          }}
          className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-300 outline-none file:mr-4 file:rounded-md file:border-0 file:bg-blue-600 file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-blue-500 disabled:opacity-50"
        />

        {selectedFile && (
          <p className="mt-2 text-xs text-slate-500">
            Selected file: {selectedFile.name}
          </p>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-300">
            Language
          </label>

          <input
            value={language}
            onChange={(event) => onLanguageChange(event.target.value)}
            disabled={isSaving}
            placeholder="Example: en, fr"
            className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
          />
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-slate-300">
            Version Label
          </label>

          <input
            value={versionLabel}
            onChange={(event) => onVersionLabelChange(event.target.value)}
            disabled={isSaving}
            placeholder="Example: English 2026"
            className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
          />
        </div>
      </div>

      <label className="flex items-center gap-3 rounded-md border border-slate-700 bg-slate-950 p-3 text-sm text-slate-300">
        <input
          type="checkbox"
          checked={isDefault}
          onChange={(event) => onIsDefaultChange(event.target.checked)}
          disabled={isSaving}
          className="h-4 w-4 rounded border-slate-600 bg-slate-900"
        />
        Set as default CV for this profile
      </label>
    </div>
  );
}
