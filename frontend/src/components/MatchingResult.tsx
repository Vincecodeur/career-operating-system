type Props = {
  matchingScore: number;
  matchingSkills: string[];
  missingSkills: string[];
};

export function MatchingResult({
  matchingScore,
  matchingSkills,
  missingSkills,
}: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <p className="text-sm text-slate-400">Matching Score</p>

        <p className="mt-2 text-4xl font-bold text-green-400">
          {matchingScore}%
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <h3 className="mb-3 text-lg font-semibold text-white">
            Matching Skills
          </h3>

          {matchingSkills.length === 0 ? (
            <p className="text-slate-400">No matching skills.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {matchingSkills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-md border border-green-700 bg-green-950 px-3 py-1 text-sm text-green-300">
                  {skill}
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <h3 className="mb-3 text-lg font-semibold text-white">
            Missing Skills
          </h3>

          {missingSkills.length === 0 ? (
            <p className="text-slate-400">No missing skills.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {missingSkills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-md border border-red-700 bg-red-950 px-3 py-1 text-sm text-red-300">
                  {skill}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
