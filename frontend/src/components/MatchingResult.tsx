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
    <section>
      <h2>Matching Result</h2>

      <p>Score: {matchingScore}%</p>

      <h3>Matching Skills</h3>

      {matchingSkills.length === 0 ? (
        <p>No matching skills.</p>
      ) : (
        <ul>
          {matchingSkills.map((skill) => (
            <li key={skill}>{skill}</li>
          ))}
        </ul>
      )}

      <h3>Missing Skills</h3>

      {missingSkills.length === 0 ? (
        <p>No missing skills.</p>
      ) : (
        <ul>
          {missingSkills.map((skill) => (
            <li key={skill}>{skill}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
