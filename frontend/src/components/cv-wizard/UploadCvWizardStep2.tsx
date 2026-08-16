type Props = {
  hardSkillsFound: number;
  softSkillsFound: number;
  experiencesFound: number;
  languagesFound: number;
  certificationsFound: number;
  conflictCount: number;
};

export function UploadCvWizardStep2({
  hardSkillsFound,
  softSkillsFound,
  experiencesFound,
  languagesFound,
  certificationsFound,
  conflictCount,
}: Props) {
  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-6">
      <h3 className="text-lg font-semibold text-white">Step 2 - Analysis</h3>

      <p className="mt-2 text-slate-400">CV analysis completed.</p>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm text-slate-400">Hard Skills Found</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {hardSkillsFound}
          </p>
        </div>
        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm text-slate-400">Soft Skills Found</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {softSkillsFound}
          </p>
        </div>

        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm text-slate-400">Experiences Found</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {experiencesFound}
          </p>
        </div>

        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm text-slate-400">Languages Found</p>

          <p className="mt-2 text-2xl font-bold text-white">{languagesFound}</p>
        </div>

        <div className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm text-slate-400">Certifications Found</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {certificationsFound}
          </p>
        </div>
      </div>

      <div className="mt-4 rounded-md border border-amber-800 bg-amber-950 p-4">
        <p className="text-sm text-amber-300">
          Conflicts detected: {conflictCount}
        </p>
      </div>
    </div>
  );
}
