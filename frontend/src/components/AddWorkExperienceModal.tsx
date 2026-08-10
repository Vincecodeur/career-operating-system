import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const addWorkExperienceSchema = z.object({
  company_name: z.string().min(1, "Company name is required."),
  job_title: z.string().min(1, "Job title is required."),
  start_date: z.string().min(1, "Start date is required."),
  end_date: z.string().optional(),
  is_current_position: z.boolean(),
  description: z.string().min(1, "Description is required."),
});

export type AddWorkExperienceFormValues = z.infer<
  typeof addWorkExperienceSchema
>;

type Props = {
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onAdd: (values: AddWorkExperienceFormValues) => Promise<void>;
};

export function AddWorkExperienceModal({
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
  } = useForm<AddWorkExperienceFormValues>({
    resolver: zodResolver(addWorkExperienceSchema),
    defaultValues: {
      company_name: "",
      job_title: "",
      start_date: "",
      end_date: "",
      is_current_position: false,
      description: "",
    },
  });

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    reset({
      company_name: "",
      job_title: "",
      start_date: "",
      end_date: "",
      is_current_position: false,
      description: "",
    });
  }, [isOpen, reset]);

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Add Work Experience</h2>

          <p className="mt-2 text-sm text-slate-400">
            Add a professional experience to the selected profile.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onAdd)} className="space-y-5">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Company Name
              </label>

              <input
                {...register("company_name")}
                disabled={isSaving}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
              />

              {errors.company_name && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.company_name.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Job Title
              </label>

              <input
                {...register("job_title")}
                disabled={isSaving}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
              />

              {errors.job_title && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.job_title.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Start Date
              </label>

              <input
                type="date"
                {...register("start_date")}
                disabled={isSaving}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
              />

              {errors.start_date && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.start_date.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                End Date
              </label>

              <input
                type="date"
                {...register("end_date")}
                disabled={isSaving}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
              />

              {errors.end_date && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.end_date.message}
                </p>
              )}
            </div>
          </div>

          <label className="flex items-center gap-3 text-sm text-slate-300">
            <input
              type="checkbox"
              {...register("is_current_position")}
              disabled={isSaving}
              className="h-4 w-4 rounded border-slate-600 bg-slate-950"
            />
            Current position
          </label>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Description
            </label>

            <textarea
              {...register("description")}
              disabled={isSaving}
              rows={5}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
            />

            {errors.description && (
              <p className="mt-1 text-xs text-red-400">
                {errors.description.message}
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
              {isSaving ? "Adding..." : "Add Experience"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
