import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const addProfileSoftSkillSchema = z.object({
  name: z.string().min(1, "Soft skill name is required."),
});

export type AddProfileSoftSkillFormValues = z.infer<
  typeof addProfileSoftSkillSchema
>;

type Props = {
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onAdd: (values: AddProfileSoftSkillFormValues) => Promise<void>;
};

export function AddProfileSoftSkillModal({
  isOpen,
  isSaving,
  error,
  onClose,
  onAdd,
}: Props) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AddProfileSoftSkillFormValues>({
    resolver: zodResolver(addProfileSoftSkillSchema),
    defaultValues: {
      name: "",
    },
  });

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    reset({
      name: "",
    });
  }, [isOpen, reset]);

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Add Soft Skill</h2>

          <p className="mt-2 text-sm text-slate-400">
            Add a manual soft skill to this profile.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onAdd)} className="space-y-5">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Soft Skill Name
            </label>

            <input
              {...register("name")}
              placeholder="Leadership, Communication, Negotiation..."
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
            />

            {errors.name && (
              <p className="mt-1 text-xs text-red-400">{errors.name.message}</p>
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
              {isSaving ? "Adding..." : "Add Soft Skill"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
