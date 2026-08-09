type OpportunityAnalysis = {
  verdict: string;
  recommendation: string;
  summary: string;
};

type ScoreExplanation = {
  criterion: string;
  score: number;
  message: string;
};

type Props = {
  matchingScore: number;
  skillsScore: number;
  experienceScore: number;
  workModeScore: number;
  locationScore: number;
  matchingSkills: string[];
  missingSkills: string[];
  strengths: string[];
  weaknesses: string[];
  explanations: ScoreExplanation[];
  opportunityAnalysis: OpportunityAnalysis;
};

export function MatchingResult({
  matchingScore,
  skillsScore,
  experienceScore,
  workModeScore,
  locationScore,
  matchingSkills,
  missingSkills,
  strengths,
  weaknesses,
  explanations,
  opportunityAnalysis,
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
            Score Details
          </h3>

          <div className="space-y-2 text-sm">
            <p>Skills: {skillsScore}%</p>
            <p>Experience: {experienceScore}%</p>
            <p>Work Mode: {workModeScore}%</p>
            <p>Location: {locationScore}%</p>
          </div>
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <h3 className="mb-3 text-lg font-semibold text-white">Strengths</h3>

          {strengths.length === 0 ? (
            <p className="text-slate-400">No strengths detected.</p>
          ) : (
            <ul className="space-y-1 text-green-300">
              {strengths.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-3 text-lg font-semibold text-white">Weaknesses</h3>

        {weaknesses.length === 0 ? (
          <p className="text-slate-400">No weaknesses detected.</p>
        ) : (
          <ul className="space-y-1 text-red-300">
            {weaknesses.map((item) => (
              <li key={item}>• {item}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-3 text-lg font-semibold text-white">
          Score Explanations
        </h3>

        {explanations.length === 0 ? (
          <p className="text-slate-400">No explanations available.</p>
        ) : (
          <div className="space-y-3">
            {explanations.map((item) => (
              <div
                key={item.criterion}
                className="rounded-md border border-slate-800 bg-slate-900 p-3">
                <p className="font-medium text-white">
                  {item.criterion} ({item.score}%)
                </p>

                <p className="mt-1 text-sm text-slate-300">{item.message}</p>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-3 text-lg font-semibold text-white">
          Opportunity Analysis
        </h3>

        <div className="space-y-3">
          <div>
            <p className="text-xs uppercase text-slate-400">Verdict</p>

            <p className="font-medium text-white">
              {opportunityAnalysis.verdict}
            </p>
          </div>

          <div>
            <p className="text-xs uppercase text-slate-400">Recommendation</p>

            <p className="font-medium text-white">
              {opportunityAnalysis.recommendation}
            </p>
          </div>

          <div>
            <p className="text-xs uppercase text-slate-400">Summary</p>

            <p className="text-slate-300">{opportunityAnalysis.summary}</p>
          </div>
        </div>
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
