import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const createProfileSchema = z.object({
  profile_name: z.string().min(1, "Profile name is required."),
  full_name: z.string().min(1, "Full name is required."),
  current_title: z.string().min(1, "Current title is required."),
  location: z.string().min(1, "Location is required."),
  years_of_experience: z
    .number()
    .int()
    .min(0, "Years of experience must be positive."),
  target_role_short_term: z.string().min(1, "Short-term target is required."),
  target_role_long_term: z.string().min(1, "Long-term target is required."),
  remote_preference: z.string().min(1, "Remote preference is required."),
  preferred_countries: z.string().min(1, "Preferred countries are required."),
});

export type CreateProfileFormValues = z.infer<typeof createProfileSchema>;

type Props = {
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onCreate: (values: CreateProfileFormValues) => Promise<void>;
};

export function CreateProfileModal({
  isOpen,
  isSaving,
  error,
  onClose,
  onCreate,
}: Props) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateProfileFormValues>({
    resolver: zodResolver(createProfileSchema),
    defaultValues: {
      profile_name: "",
      full_name: "",
      current_title: "",
      location: "",
      years_of_experience: 0,
      target_role_short_term: "",
      target_role_long_term: "",
      remote_preference: "",
      preferred_countries: "",
    },
  });

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    reset({
      profile_name: "",
      full_name: "",
      current_title: "",
      location: "",
      years_of_experience: 0,
      target_role_short_term: "",
      target_role_long_term: "",
      remote_preference: "",
      preferred_countries: "",
    });
  }, [isOpen, reset]);

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">New Profile</h2>

          <p className="mt-2 text-sm text-slate-400">
            Create a new structured candidate profile for the Career Operating
            System.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onCreate)} className="space-y-5">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Profile Name
              </label>

              <input
                {...register("profile_name")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.profile_name && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.profile_name.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Full Name
              </label>

              <input
                {...register("full_name")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.full_name && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.full_name.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Current Title
              </label>

              <input
                {...register("current_title")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.current_title && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.current_title.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Location
              </label>

              <input
                {...register("location")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.location && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.location.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Years of Experience
              </label>

              <input
                type="number"
                {...register("years_of_experience", {
                  valueAsNumber: true,
                })}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.years_of_experience && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.years_of_experience.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Remote Preference
              </label>

              <input
                {...register("remote_preference")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.remote_preference && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.remote_preference.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Short-Term Target Role
              </label>

              <input
                {...register("target_role_short_term")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.target_role_short_term && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.target_role_short_term.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Long-Term Target Role
              </label>

              <input
                {...register("target_role_long_term")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
              />

              {errors.target_role_long_term && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.target_role_long_term.message}
                </p>
              )}
            </div>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Preferred Countries
            </label>

            <input
              {...register("preferred_countries")}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
            />

            {errors.preferred_countries && (
              <p className="mt-1 text-xs text-red-400">
                {errors.preferred_countries.message}
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
              {isSaving ? "Creating..." : "Create Profile"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
