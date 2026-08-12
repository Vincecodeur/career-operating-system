type Props = {
  skills: number;
  experiences: number;
  languages: number;
  certifications: number;
  resolvedConflicts: number;
  totalConflicts: number;
};

export function WizardSummary({
  skills,
  experiences,
  languages,
  certifications,
  resolvedConflicts,
  totalConflicts,
}: Props) {
  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
      <h4 className="font-semibold text-white">Import Summary</h4>

      <div className="mt-4 space-y-2 text-sm text-slate-300">
        <p>Skills: {skills}</p>

        <p>Experiences: {experiences}</p>

        <p>Languages: {languages}</p>

        <p>Certifications: {certifications}</p>

        <p>
          Conflicts Resolved: {resolvedConflicts}/{totalConflicts}
        </p>
      </div>
    </div>
  );
}
