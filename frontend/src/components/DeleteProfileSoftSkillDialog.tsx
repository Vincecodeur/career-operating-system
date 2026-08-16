import type { ProfileSoftSkill } from "../services/api";

type Props = {
  softSkill: ProfileSoftSkill | null;
  isOpen: boolean;
  isDeleting: boolean;
  error: string | null;
  onClose: () => void;
  onConfirm: () => Promise<void>;
};

export function DeleteProfileSoftSkillDialog({
  softSkill,
  isOpen,
  isDeleting,
  error,
  onClose,
  onConfirm,
}: Props) {
  if (!isOpen || !softSkill) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white">Remove Soft Skill</h2>

        <p className="mt-3 text-sm text-slate-400">
          Are you sure you want to remove this soft skill from the profile?
        </p>

        <div className="mt-4 rounded-md border border-slate-700 bg-slate-950 p-3 text-sm text-slate-300">
          {softSkill.name}
        </div>

        {error && (
          <div className="mt-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <div className="mt-6 flex justify-end gap-3 border-t border-slate-700 pt-5">
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
            className="rounded-md bg-red-700 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600 disabled:opacity-50">
            {isDeleting ? "Removing..." : "Remove"}
          </button>
        </div>
      </div>
    </div>
  );
}
