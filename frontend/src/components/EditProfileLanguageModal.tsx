import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

type Language = {
  id: number;
  name: string;
  created_at: string;
};

type ProfileLanguage = {
  profile_id: number;
  language_id: number;
  proficiency_level: string;
  created_at: string;
};

const editProfileLanguageSchema = z.object({
  proficiency_level: z.string().min(1, "Proficiency level is required."),
});

export type EditProfileLanguageFormValues = z.infer<
  typeof editProfileLanguageSchema
>;

type Props = {
  profileLanguage: ProfileLanguage | null;
  language: Language | null;
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onSave: (values: EditProfileLanguageFormValues) => Promise<void>;
};

export function EditProfileLanguageModal({
  profileLanguage,
  language,
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
  } = useForm<EditProfileLanguageFormValues>({
    resolver: zodResolver(editProfileLanguageSchema),
    defaultValues: {
      proficiency_level: "B2",
    },
  });

  useEffect(() => {
    if (!isOpen || !profileLanguage) {
      return;
    }

    reset({
      proficiency_level: profileLanguage.proficiency_level ?? "B2",
    });
  }, [isOpen, profileLanguage, reset]);

  if (!isOpen || !profileLanguage) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Edit Language</h2>

          <p className="mt-2 text-sm text-slate-400">
            Update the profile-specific language proficiency.
          </p>
        </div>

        <div className="mb-5 rounded-md border border-slate-700 bg-slate-950 p-4">
          <p className="text-sm uppercase text-slate-500">Language</p>

          <p className="mt-1 font-semibold text-white">
            {language?.name ?? `Language ${profileLanguage.language_id}`}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            Language selection cannot be changed because it is part of the
            profile language relationship.
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
              Proficiency Level
            </label>

            <select
              {...register("proficiency_level")}
              disabled={isSaving}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50">
              <option value="A1">A1</option>
              <option value="A2">A2</option>
              <option value="B1">B1</option>
              <option value="B2">B2</option>
              <option value="C1">C1</option>
              <option value="C2">C2</option>
              <option value="Native">Native</option>
            </select>

            {errors.proficiency_level && (
              <p className="mt-1 text-xs text-red-400">
                {errors.proficiency_level.message}
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
