import { useEffect, useMemo } from "react";
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

const addProfileCertificationSchema = z.object({
  certification_id: z.number().int().min(1, "Certification is required."),
  obtained_date: z.string().optional(),
  expiration_date: z.string().optional(),
  credential_id: z.string().optional(),
});

export type AddProfileCertificationFormValues = z.infer<
  typeof addProfileCertificationSchema
>;

type Props = {
  certifications: Certification[];
  profileCertifications: ProfileCertification[];
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onAdd: (values: AddProfileCertificationFormValues) => Promise<void>;
};

export function AddProfileCertificationModal({
  certifications,
  profileCertifications,
  isOpen,
  isSaving,
  error,
  onClose,
  onAdd,
}: Props) {
  const assignedCertificationIds = new Set(
    profileCertifications.map(
      (profileCertification) => profileCertification.certification_id,
    ),
  );

  const availableCertifications = useMemo(
    () =>
      certifications.filter(
        (certification) => !assignedCertificationIds.has(certification.id),
      ),
    [certifications, profileCertifications],
  );

  const firstAvailableCertificationId = availableCertifications[0]?.id ?? 0;

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AddProfileCertificationFormValues>({
    resolver: zodResolver(addProfileCertificationSchema),
    defaultValues: {
      certification_id: firstAvailableCertificationId,
      obtained_date: "",
      expiration_date: "",
      credential_id: "",
    },
  });

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    reset({
      certification_id: firstAvailableCertificationId,
      obtained_date: "",
      expiration_date: "",
      credential_id: "",
    });
  }, [isOpen, firstAvailableCertificationId, reset]);

  if (!isOpen) {
    return null;
  }

  const hasAvailableCertifications = availableCertifications.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-2xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white">Add Certification</h2>

          <p className="mt-2 text-sm text-slate-400">
            Add an existing certification to the selected profile.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        {!hasAvailableCertifications && (
          <div className="mb-4 rounded-md border border-amber-800 bg-amber-950 p-3 text-sm text-amber-300">
            All catalog certifications are already linked to this profile.
          </div>
        )}

        <form onSubmit={handleSubmit(onAdd)} className="space-y-5">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-300">
              Certification
            </label>

            <select
              {...register("certification_id", {
                valueAsNumber: true,
              })}
              disabled={!hasAvailableCertifications || isSaving}
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500 disabled:opacity-50">
              {availableCertifications.map((certification) => (
                <option key={certification.id} value={certification.id}>
                  {certification.name}
                  {certification.issuing_organization
                    ? ` - ${certification.issuing_organization}`
                    : ""}
                </option>
              ))}
            </select>

            {errors.certification_id && (
              <p className="mt-1 text-xs text-red-400">
                {errors.certification_id.message}
              </p>
            )}
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-300">
                Obtained Date
              </label>

              <input
                type="date"
                {...register("obtained_date")}
                disabled={!hasAvailableCertifications || isSaving}
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
                disabled={!hasAvailableCertifications || isSaving}
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
              disabled={!hasAvailableCertifications || isSaving}
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
              disabled={isSaving || !hasAvailableCertifications}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
              {isSaving ? "Adding..." : "Add Certification"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
