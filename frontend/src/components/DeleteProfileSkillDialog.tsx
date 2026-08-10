type Skill = {
  id: number;
  name: string;
  category: string | null;
  created_at: string;
};

type ProfileSkill = {
  profile_id: number;
  skill_id: number;
  years_of_experience: number | null;
  self_assessment_level: string | null;
  created_at: string;
};

type Props = {
  profileSkill: ProfileSkill | null;
  skill: Skill | null;
  isOpen: boolean;
  isDeleting: boolean;
  error: string | null;
  onClose: () => void;
  onConfirm: () => Promise<void>;
};

export function DeleteProfileSkillDialog({
  profileSkill,
  skill,
  isOpen,
  isDeleting,
  error,
  onClose,
  onConfirm,
}: Props) {
  if (!isOpen || !profileSkill) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-lg rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white">Remove Skill</h2>

        <p className="mt-3 text-sm text-slate-400">
          This action will remove the skill from this profile. The global skill
          catalog will not be modified.
        </p>

        <div className="mt-5 rounded-md border border-slate-700 bg-slate-950 p-4">
          <p className="text-sm uppercase text-slate-500">Skill</p>

          <p className="mt-1 font-semibold text-white">
            {skill?.name ?? `Skill ${profileSkill.skill_id}`}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            {profileSkill.self_assessment_level ?? "No level"} ·{" "}
            {profileSkill.years_of_experience ?? 0} years
          </p>
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
            {isDeleting ? "Removing..." : "Remove Skill"}
          </button>
        </div>
      </div>
    </div>
  );
}
