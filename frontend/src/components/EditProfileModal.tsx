import { useEffect } from "react";
import Select from "react-select";
import type { MultiValue } from "react-select";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

type Profile = {
  id: number;
  profile_name: string;
  full_name: string;
  current_title: string | null;
  location: string | null;
  years_of_experience: number | null;
  target_role_short_term: string | null;
  target_role_long_term: string | null;
  remote_preference: string | null;
  preferred_countries: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  professional_summary: string | null;
  career_motivations: string | null;
  preferred_environment: string | null;
  non_negotiables: string | null;
  additional_context: string | null;
};

const profileSchema = z.object({
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
  professional_summary: z.string().optional(),
  career_motivations: z.string().optional(),
  preferred_environment: z.string().optional(),
  non_negotiables: z.string().optional(),
  additional_context: z.string().optional(),
});

export type ProfileFormValues = z.infer<typeof profileSchema>;

type CountryOption = {
  value: string;
  label: string;
};

type Props = {
  profile: Profile | null;
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onSave: (values: ProfileFormValues) => Promise<void>;

  workModes: {
    id: number;
    code: string;
    name: string;
  }[];

  countries: {
    id: number;
    code: string;
    name: string;
  }[];
};

export function EditProfileModal({
  profile,
  isOpen,
  isSaving,
  error,
  onClose,
  onSave,
  workModes,
  countries,
}: Props) {
  const {
    control,
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProfileFormValues>({
    resolver: zodResolver(profileSchema),
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
      professional_summary: "",
      career_motivations: "",
      preferred_environment: "",
      non_negotiables: "",
      additional_context: "",
    },
  });

  useEffect(() => {
    if (!profile) {
      return;
    }

    reset({
      profile_name: profile.profile_name,
      full_name: profile.full_name,
      current_title: profile.current_title ?? "",
      location: profile.location ?? "",
      years_of_experience: profile.years_of_experience ?? 0,
      target_role_short_term: profile.target_role_short_term ?? "",
      target_role_long_term: profile.target_role_long_term ?? "",
      remote_preference: profile.remote_preference ?? "",
      preferred_countries: profile.preferred_countries ?? "",
      professional_summary: profile.professional_summary ?? "",
      career_motivations: profile.career_motivations ?? "",
      preferred_environment: profile.preferred_environment ?? "",
      non_negotiables: profile.non_negotiables ?? "",
      additional_context: profile.additional_context ?? "",
    });
  }, [profile, reset]);

  if (!isOpen || !profile) {
    return null;
  }

  const countryOptions: CountryOption[] = countries.map((country) => ({
    value: country.code,
    label: country.name,
  }));

  function getSelectedCountryOptions(value: string): CountryOption[] {
    const selectedCodes = value
      .split(",")
      .map((code) => code.trim())
      .filter((code) => code.length > 0);

    return countryOptions.filter((option) =>
      selectedCodes.includes(option.value),
    );
  }

  function serializeCountryOptions(
    selectedOptions: MultiValue<CountryOption>,
  ): string {
    return selectedOptions.map((option) => option.value).join(",");
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Edit Profile</h2>

          <p className="mt-2 text-sm text-slate-400">
            Update the structured profile information used by the Career
            Operating System.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSave)} className="space-y-5">
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

              <select
                {...register("remote_preference")}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500">
                <option value="">Select work mode</option>

                {workModes.map((workMode) => (
                  <option key={workMode.id} value={workMode.code}>
                    {workMode.name}
                  </option>
                ))}
              </select>

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

            <Controller
              name="preferred_countries"
              control={control}
              render={({ field }) => (
                <Select
                  isMulti
                  options={countryOptions}
                  value={getSelectedCountryOptions(field.value)}
                  onChange={(selectedOptions) => {
                    field.onChange(serializeCountryOptions(selectedOptions));
                  }}
                  onBlur={field.onBlur}
                  placeholder="Select countries"
                  className="text-slate-900"
                />
              )}
            />

            {errors.preferred_countries && (
              <p className="mt-1 text-xs text-red-400">
                {errors.preferred_countries.message}
              </p>
            )}
          </div>
          <div className="border-t border-slate-700 pt-5">
            <h3 className="mb-4 text-lg font-semibold text-white">
              Additional Profile Context
            </h3>

            <div className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-slate-300">
                  Professional Summary
                </label>

                <textarea
                  {...register("professional_summary")}
                  rows={3}
                  className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-300">
                  Career Motivations
                </label>

                <textarea
                  {...register("career_motivations")}
                  rows={3}
                  className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-300">
                  Preferred Environment
                </label>

                <textarea
                  {...register("preferred_environment")}
                  rows={3}
                  className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-300">
                  Non-Negotiables
                </label>

                <textarea
                  {...register("non_negotiables")}
                  rows={3}
                  className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-300">
                  Additional Context
                </label>

                <textarea
                  {...register("additional_context")}
                  rows={4}
                  className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                />
              </div>
            </div>
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
