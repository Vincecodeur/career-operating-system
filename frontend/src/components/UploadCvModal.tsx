import { useEffect, useState } from "react";

export type UploadCvFormValues = {
  file: File;
  language: string;
  versionLabel: string;
  isDefault: boolean;
};

type Props = {
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onUpload: (values: UploadCvFormValues) => Promise<void>;
};

export function UploadCvModal({
  isOpen,
  isSaving,
  error,
  onClose,
  onUpload,
}: Props) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("");
  const [versionLabel, setVersionLabel] = useState("");
  const [isDefault, setIsDefault] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    setSelectedFile(null);
    setLanguage("");
    setVersionLabel("");
    setIsDefault(false);
    setLocalError(null);
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setLocalError("Please select a CV file.");
      return;
    }

    setLocalError(null);

    await onUpload({
      file: selectedFile,
      language,
      versionLabel,
      isDefault,
    });
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Upload CV</h2>

          <p className="mt-2 text-sm text-slate-400">
            Attach a CV document to the selected profile.
          </p>
        </div>

        {(error || localError) && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {localError ?? error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
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
                setSelectedFile(file);
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
                onChange={(event) => setLanguage(event.target.value)}
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
                onChange={(event) => setVersionLabel(event.target.value)}
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
              onChange={(event) => setIsDefault(event.target.checked)}
              disabled={isSaving}
              className="h-4 w-4 rounded border-slate-600 bg-slate-900"
            />
            Set as default CV for this profile
          </label>

          <div className="flex justify-end gap-3 border-t border-slate-700 pt-5">
            <button
              type="button"
              onClick={onClose}
              disabled={isSaving}
              className="rounded-md border border-slate-600 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 disabled:opacity-50">
              Cancel
            </button>

            <button
              type="submit"
              disabled={isSaving}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
              {isSaving ? "Uploading..." : "Upload CV"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
