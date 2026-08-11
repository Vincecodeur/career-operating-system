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

type Props = {
  profileCertification: ProfileCertification | null;
  certification: Certification | null;
  isOpen: boolean;
  isDeleting: boolean;
  error: string | null;
  onClose: () => void;
  onConfirm: () => Promise<void>;
};

export function DeleteProfileCertificationDialog({
  profileCertification,
  certification,
  isOpen,
  isDeleting,
  error,
  onClose,
  onConfirm,
}: Props) {
  if (!isOpen || !profileCertification) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-lg rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white">Remove Certification</h2>

        <p className="mt-3 text-sm text-slate-400">
          This action will remove the certification from this profile. The
          global certification catalog will not be modified.
        </p>

        <div className="mt-5 rounded-md border border-slate-700 bg-slate-950 p-4">
          <p className="text-sm uppercase text-slate-500">Certification</p>

          <p className="mt-1 font-semibold text-white">
            {certification?.name ??
              `Certification ${profileCertification.certification_id}`}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            {certification?.issuing_organization ?? "Unknown issuer"}
          </p>

          {profileCertification.credential_id && (
            <p className="mt-1 text-xs text-slate-500">
              Credential: {profileCertification.credential_id}
            </p>
          )}
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
            {isDeleting ? "Removing..." : "Remove Certification"}
          </button>
        </div>
      </div>
    </div>
  );
}
