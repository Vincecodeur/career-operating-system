import type { Cv } from "../services/api";

type Props = {
  cv: Cv | null;
  isOpen: boolean;
  isDeleting: boolean;
  error: string | null;
  onClose: () => void;
  onConfirm: () => Promise<void>;
};

function formatFileSize(fileSizeBytes: number) {
  if (fileSizeBytes < 1024) {
    return `${fileSizeBytes} B`;
  }

  if (fileSizeBytes < 1024 * 1024) {
    return `${Math.round(fileSizeBytes / 1024)} KB`;
  }

  return `${(fileSizeBytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function DeleteCvDialog({
  cv,
  isOpen,
  isDeleting,
  error,
  onClose,
  onConfirm,
}: Props) {
  if (!isOpen || !cv) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-lg rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white">Delete CV</h2>

        <p className="mt-3 text-sm text-slate-400">
          This action will permanently remove the CV from this profile.
        </p>

        <div className="mt-5 rounded-md border border-slate-700 bg-slate-950 p-4">
          <p className="text-sm uppercase text-slate-500">CV</p>

          <p className="mt-1 font-semibold text-white">
            {cv.original_file_name}
          </p>

          <div className="mt-2 space-y-1 text-sm text-slate-400">
            <p>Version: {cv.version_label ?? "No version label"}</p>

            <p>Language: {cv.language ?? "Unknown"}</p>

            <p>Size: {formatFileSize(cv.file_size_bytes)}</p>

            <p>Status: {cv.parsing_status}</p>

            {cv.is_default && (
              <p className="font-medium text-blue-300">
                This CV is currently the default CV.
              </p>
            )}
          </div>
        </div>

        {error && (
          <div className="mt-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            disabled={isDeleting}
            className="rounded-md border border-slate-600 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 disabled:opacity-50">
            Cancel
          </button>

          <button
            type="button"
            onClick={onConfirm}
            disabled={isDeleting}
            className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50">
            {isDeleting ? "Deleting..." : "Delete CV"}
          </button>
        </div>
      </div>
    </div>
  );
}
