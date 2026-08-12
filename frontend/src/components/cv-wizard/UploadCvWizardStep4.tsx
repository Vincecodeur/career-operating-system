import type { ProfileEnrichmentProposal } from "../../services/api";

type Props = {
  proposals: ProfileEnrichmentProposal[];
  selectedProposalIds: number[];
  editedExperienceValues: Record<number, string>;
};

function filterSelected(
  proposals: ProfileEnrichmentProposal[],
  selectedProposalIds: number[],
) {
  return proposals.filter((proposal) =>
    selectedProposalIds.includes(proposal.id),
  );
}

export function UploadCvWizardStep4({
  proposals,
  selectedProposalIds,
  editedExperienceValues,
}: Props) {
  const selectedProposals = filterSelected(proposals, selectedProposalIds);

  const selectedSkills = selectedProposals.filter(
    (proposal) => proposal.proposal_type === "SKILL",
  );

  const selectedLanguages = selectedProposals.filter(
    (proposal) => proposal.proposal_type === "LANGUAGE",
  );

  const selectedCertifications = selectedProposals.filter(
    (proposal) => proposal.proposal_type === "CERTIFICATION",
  );

  const selectedExperiences = selectedProposals.filter(
    (proposal) => proposal.proposal_type === "EXPERIENCE",
  );

  const excludedCount = proposals.length - selectedProposals.length;

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-6">
      <h3 className="text-lg font-semibold text-white">Step 4 - Summary</h3>

      <p className="mt-2 text-sm text-slate-400">
        Review the final changes before applying them.
      </p>

      <div className="mt-6 rounded-md border border-slate-800 bg-slate-900 p-4">
        <div className="grid gap-2 md:grid-cols-4">
          <p>Selected: {selectedProposals.length}</p>
          <p>Excluded: {excludedCount}</p>
          <p>Skills: {selectedSkills.length}</p>
          <p>Experiences: {selectedExperiences.length}</p>
        </div>
      </div>

      <div className="mt-8 space-y-8">
        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Selected Skills
          </h4>

          <div className="space-y-2">
            {selectedSkills.map((proposal) => (
              <div
                key={proposal.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-3">
                {proposal.proposed_value}
              </div>
            ))}
          </div>
        </section>

        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Selected Languages
          </h4>

          <div className="space-y-2">
            {selectedLanguages.map((proposal) => (
              <div
                key={proposal.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-3">
                {proposal.proposed_value}
              </div>
            ))}
          </div>
        </section>

        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Edited Experiences
          </h4>

          <div className="space-y-4">
            {selectedExperiences.map((proposal) => (
              <div
                key={proposal.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">Original</p>

                <div className="mt-2 rounded border border-slate-800 bg-slate-950 p-3 text-sm text-slate-400">
                  {proposal.proposed_value}
                </div>

                <p className="mt-4 text-xs uppercase text-slate-500">Final</p>

                <div className="mt-2 rounded border border-slate-700 bg-slate-950 p-3 text-sm text-slate-200">
                  {editedExperienceValues[proposal.id] ??
                    proposal.proposed_value}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Certifications
          </h4>

          <div className="space-y-2">
            {selectedCertifications.map((proposal) => (
              <div
                key={proposal.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-3">
                {proposal.proposed_value}
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
