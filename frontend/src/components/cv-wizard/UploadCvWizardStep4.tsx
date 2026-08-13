import type { ProfileEnrichmentProposal } from "../../services/api";

type Props = {
  proposals: ProfileEnrichmentProposal[];
  selectedProposalIds: number[];
  editedExperienceValues: Record<number, string>;
  conflictResolutions: Record<
    number,
    {
      mode: "current" | "proposed" | "custom";
      customValue: string;
    }
  >;

  onConflictResolutionChange: (
    proposalId: number,
    mode: "current" | "proposed" | "custom",
    customValue?: string,
  ) => void;
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
  conflictResolutions,
  onConflictResolutionChange,
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
  const excludedProposals = proposals.filter(
    (proposal) => !selectedProposalIds.includes(proposal.id),
  );

  const conflictProposals = selectedProposals.filter(
    (proposal) => proposal.conflict_detected,
  );

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
            Excluded Items ({excludedProposals.length})
          </h4>

          {excludedProposals.length === 0 ? (
            <div className="rounded-md border border-slate-800 bg-slate-900 p-3">
              No excluded items.
            </div>
          ) : (
            <div className="space-y-2">
              {excludedProposals.map((proposal) => (
                <div
                  key={proposal.id}
                  className="rounded-md border border-red-900 bg-red-950/30 p-3">
                  {proposal.proposed_value}
                </div>
              ))}
            </div>
          )}
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
            Conflicts ({conflictProposals.length})
          </h4>

          {conflictProposals.length === 0 ? (
            <div className="rounded-md border border-slate-800 bg-slate-900 p-3">
              No conflicts detected.
            </div>
          ) : (
            <div className="space-y-3">
              {conflictProposals.map((proposal) => (
                <div
                  key={proposal.id}
                  className="rounded-md border border-amber-900 bg-amber-950/30 p-4">
                  <p className="font-medium text-white">
                    {proposal.proposed_value}
                  </p>

                  <p className="mt-2 text-sm text-amber-300">
                    Conflict detected
                  </p>

                  {proposal.current_profile_value && (
                    <div className="mt-3 text-sm text-slate-300">
                      Current value:
                      <div className="mt-4 space-y-3">
                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            checked={
                              (conflictResolutions[proposal.id]?.mode ??
                                "current") === "current"
                            }
                            onChange={() =>
                              onConflictResolutionChange(proposal.id, "current")
                            }
                          />
                          <span>Keep current value</span>
                        </label>

                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            checked={
                              conflictResolutions[proposal.id]?.mode ===
                              "proposed"
                            }
                            onChange={() =>
                              onConflictResolutionChange(
                                proposal.id,
                                "proposed",
                              )
                            }
                          />
                          <span>Use CV value: {proposal.proposed_value}</span>
                        </label>

                        <label className="flex items-center gap-2">
                          <input
                            type="radio"
                            checked={
                              conflictResolutions[proposal.id]?.mode ===
                              "custom"
                            }
                            onChange={() =>
                              onConflictResolutionChange(proposal.id, "custom")
                            }
                          />
                          <span>Custom value</span>
                        </label>

                        {conflictResolutions[proposal.id]?.mode ===
                          "custom" && (
                          <input
                            type="text"
                            value={
                              conflictResolutions[proposal.id]?.customValue ??
                              ""
                            }
                            onChange={(event) =>
                              onConflictResolutionChange(
                                proposal.id,
                                "custom",
                                event.target.value,
                              )
                            }
                            className="w-full rounded border border-slate-700 bg-slate-900 p-2"
                          />
                        )}
                      </div>
                      <div className="mt-1 rounded border border-slate-800 bg-slate-950 p-2">
                        {proposal.current_profile_value}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
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
