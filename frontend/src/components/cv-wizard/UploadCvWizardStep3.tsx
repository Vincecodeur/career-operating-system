export function UploadCvWizardStep3() {
  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-6">
      <h3 className="text-lg font-semibold text-white">
        Step 3 - Review & Edit
      </h3>

      <p className="mt-2 text-slate-400">
        Review the detected information before updating the profile.
      </p>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <h4 className="font-semibold text-white">Skills</h4>

          <p className="mt-2 text-sm text-slate-400">
            Select skills to import.
          </p>
        </div>

        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <h4 className="font-semibold text-white">Languages</h4>

          <p className="mt-2 text-sm text-slate-400">
            Select languages to import.
          </p>
        </div>

        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <h4 className="font-semibold text-white">Certifications</h4>

          <p className="mt-2 text-sm text-slate-400">
            Select certifications to import.
          </p>
        </div>

        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <h4 className="font-semibold text-white">Work Experience</h4>

          <p className="mt-2 text-sm text-slate-400">
            Review and edit experiences before import.
          </p>
        </div>
      </div>
    </div>
  );
}
