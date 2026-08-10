import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

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

const editProfileSkillSchema = z.object({
  years_of_experience: z
    .number()
    .int()
    .min(0, "Years of experience must be positive."),
  self_assessment_level: z.string().min(1, "Assessment level is required."),
});

export type EditProfileSkillFormValues = z.infer<typeof editProfileSkillSchema>;

type Props = {
  profileSkill: ProfileSkill | null;
  skill: Skill | null;
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onSave: (values: EditProfileSkillFormValues) => Promise<void>;
};

export function EditProfileSkillModal({
  profileSkill,
  skill,
  isOpen,
  isSaving,
  error,
  onClose,
  onSave,
}: Props) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<EditProfileSkillFormValues>({
    resolver: zodResolver(editProfileSkillSchema),
    defaultValues: {
      years_of_experience: 0,
      self_assessment_level: "Intermediate",
    },
  });

  useEffect(() => {
    if (!isOpen || !profileSkill) {
      return;
    }

    reset({
      years_of_experience: profileSkill.years_of_experience ?? 0,
      self_assessment_level:
        profileSkill.self_assessment_level ?? "Intermediate",
    });
  }, [isOpen, profileSkill, reset]);

  if (!isOpen || !profileSkill) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Edit Skill</h2>

          <p className="mt-2 text-sm text-slate-400">
            Update the profile-specific skill information.
          </p>
        </div>

        <div className="mb-5 rounded-md border border-slate-700 bg-slate-950 p-4">
          <p className="text-sm uppercase text-slate-500">Skill</p>

          <p className="mt-1 font-semibold text-white">
            {skill?.name ?? `Skill ${profileSkill.skill_id}`}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            {skill?.category ?? "No category"}
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSave)} className="space-y-5">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Years of Experience
            </label>

            <input
              type="number"
              {...register("years_of_experience", {
                valueAsNumber: true,
              })}
              disabled={isSaving}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
            />

            {errors.years_of_experience && (
              <p className="mt-1 text-xs text-red-400">
                {errors.years_of_experience.message}
              </p>
            )}
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Self Assessment Level
            </label>

            <select
              {...register("self_assessment_level")}
              disabled={isSaving}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50">
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
              <option value="Expert">Expert</option>
            </select>

            {errors.self_assessment_level && (
              <p className="mt-1 text-xs text-red-400">
                {errors.self_assessment_level.message}
              </p>
            )}
          </div>

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
              {isSaving ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
