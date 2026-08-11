import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

type Certification = {
  id: number;
  name: string;
  issuing_organization: string | null;
  created_at: string;
};

type ProfileCertification = {
  profile_id: number;
  certification_id: number;
  obtained_date: string | null;
  expiration_date: string | null;
  credential_id: string | null;
  created_at: string;
};

const editProfileCertificationSchema = z.object({
  obtained_date: z.string().optional(),
  expiration_date: z.string().optional(),
  credential_id: z.string().optional(),
});

export type EditProfileCertificationFormValues = z.infer<
  typeof editProfileCertificationSchema
>;

type Props = {
  profileCertification: ProfileCertification | null;
  certification: Certification | null;
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onSave: (values: EditProfileCertificationFormValues) => Promise<void>;
};

export function EditProfileCertificationModal({
  profileCertification,
  certification,
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
  } = useForm<EditProfileCertificationFormValues>({
    resolver: zodResolver(editProfileCertificationSchema),
    defaultValues: {
      obtained_date: "",
      expiration_date: "",
      credential_id: "",
    },
  });

  useEffect(() => {
    if (!isOpen || !profileCertification) {
      return;
    }

    reset({
      obtained_date: profileCertification.obtained_date ?? "",
      expiration_date: profileCertification.expiration_date ?? "",
      credential_id: profileCertification.credential_id ?? "",
    });
  }, [isOpen, profileCertification, reset]);

  if (!isOpen || !profileCertification) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Edit Certification</h2>

          <p className="mt-2 text-sm text-slate-400">
            Update the profile-specific certification information.
          </p>
        </div>

        <div className="mb-5 rounded-md border border-slate-700 bg-slate-950 p-4">
          <p className="text-sm uppercase text-slate-500">Certification</p>

          <p className="mt-1 font-semibold text-white">
            {certification?.name ??
              `Certification ${profileCertification.certification_id}`}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            {certification?.issuing_organization ?? "Unknown issuer"}
          </p>

          <p className="mt-2 text-sm text-slate-500">
            Certification selection cannot be changed because it is part of the
            profile certification relationship.
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
                Obtained Date
              </label>

              <input
                type="date"
                {...register("obtained_date")}
                disabled={isSaving}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
              />

              {errors.obtained_date && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.obtained_date.message}
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Expiration Date
              </label>

              <input
                type="date"
                {...register("expiration_date")}
                disabled={isSaving}
                className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
              />

              {errors.expiration_date && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.expiration_date.message}
                </p>
              )}
            </div>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Credential ID
            </label>

            <input
              {...register("credential_id")}
              disabled={isSaving}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50"
            />

            {errors.credential_id && (
              <p className="mt-1 text-xs text-red-400">
                {errors.credential_id.message}
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
