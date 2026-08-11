import { useEffect, useMemo } from "react";
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

const addProfileLanguageSchema = z.object({
  language_id: z.number().int().min(1, "Language is required."),
  proficiency_level: z.string().min(1, "Proficiency level is required."),
});

export type AddProfileLanguageFormValues = z.infer<
  typeof addProfileLanguageSchema
>;

type Props = {
  languages: Language[];
  profileLanguages: ProfileLanguage[];
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onAdd: (values: AddProfileLanguageFormValues) => Promise<void>;
};

export function AddProfileLanguageModal({
  languages,
  profileLanguages,
  isOpen,
  isSaving,
  error,
  onClose,
  onAdd,
}: Props) {
  const assignedLanguageIds = new Set(
    profileLanguages.map((profileLanguage) => profileLanguage.language_id),
  );

  const availableLanguages = useMemo(
    () => languages.filter((language) => !assignedLanguageIds.has(language.id)),
    [languages, profileLanguages],
  );

  const firstAvailableLanguageId = availableLanguages[0]?.id ?? 0;

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AddProfileLanguageFormValues>({
    resolver: zodResolver(addProfileLanguageSchema),
    defaultValues: {
      language_id: firstAvailableLanguageId,
      proficiency_level: "B2",
    },
  });

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    reset({
      language_id: firstAvailableLanguageId,
      proficiency_level: "B2",
    });
  }, [isOpen, firstAvailableLanguageId, reset]);

  if (!isOpen) {
    return null;
  }

  const hasAvailableLanguages = availableLanguages.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Add Language</h2>

          <p className="mt-2 text-sm text-slate-400">
            Add an existing language to the selected profile.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        {!hasAvailableLanguages && (
          <div className="mb-4 rounded-md border border-amber-800 bg-amber-950 p-3 text-sm text-amber-300">
            All catalog languages are already linked to this profile.
          </div>
        )}

        <form onSubmit={handleSubmit(onAdd)} className="space-y-5">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Language
            </label>

            <select
              {...register("language_id", {
                valueAsNumber: true,
              })}
              disabled={!hasAvailableLanguages || isSaving}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50">
              {availableLanguages.map((language) => (
                <option key={language.id} value={language.id}>
                  {language.name}
                </option>
              ))}
            </select>

            {errors.language_id && (
              <p className="mt-1 text-xs text-red-400">
                {errors.language_id.message}
              </p>
            )}
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Proficiency Level
            </label>

            <select
              {...register("proficiency_level")}
              disabled={!hasAvailableLanguages || isSaving}
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
              disabled={isSaving || !hasAvailableLanguages}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
              {isSaving ? "Adding..." : "Add Language"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
