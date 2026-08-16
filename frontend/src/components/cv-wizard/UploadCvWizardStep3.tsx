import type { ProfileEnrichmentProposal, Skill } from "../../services/api";

type Props = {
  proposals: ProfileEnrichmentProposal[];
  selectedProposalIds: number[];
  editedExperienceValues: Record<number, string>;
  skillsCatalog: Skill[];
  skillMappings: Record<number, number>;
  skillClassifications: Record<number, "HARD_SKILL" | "SOFT_SKILL">;

  onToggleProposal: (proposalId: number) => void;
  onExperienceValueChange: (proposalId: number, value: string) => void;
  onSkillMappingChange: (proposalId: number, skillId: number | null) => void;
  onSkillClassificationChange: (
    proposalId: number,
    classification: "HARD_SKILL" | "SOFT_SKILL",
  ) => void;
};

function filterProposalsByType(
  proposals: ProfileEnrichmentProposal[],
  proposalType: string,
) {
  return proposals.filter(
    (proposal) => proposal.proposal_type === proposalType,
  );
}

function getProposedValue(proposal: ProfileEnrichmentProposal) {
  return proposal.proposed_value || proposal.observed_value;
}

function renderEmptyState(label: string) {
  return (
    <p className="rounded-md border border-slate-800 bg-slate-900 p-4 text-sm text-slate-400">
      No {label.toLowerCase()} detected.
    </p>
  );
}

function renderSimpleProposalList(
  proposals: ProfileEnrichmentProposal[],
  emptyLabel: string,
  selectedProposalIds: number[],
  skillsCatalog: Skill[],
  skillMappings: Record<number, number>,
  skillClassifications: Record<number, "HARD_SKILL" | "SOFT_SKILL">,
  onToggle: (proposalId: number) => void,
  onSkillClassificationChange: (
    proposalId: number,
    classification: "HARD_SKILL" | "SOFT_SKILL",
  ) => void,
  onSkillMappingChange: (proposalId: number, skillId: number | null) => void,
) {
  if (proposals.length === 0) {
    return renderEmptyState(emptyLabel);
  }

  return (
    <div className="space-y-3">
      {proposals.map((proposal) => (
        <div
          key={proposal.id}
          className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-start gap-3">
            <input
              type="checkbox"
              checked={selectedProposalIds.includes(proposal.id)}
              disabled={
                proposal.proposal_type === "SKILL" &&
                proposal.reference_id === null &&
                !skillMappings[proposal.id]
              }
              onChange={() => onToggle(proposal.id)}
              className="mt-1"
            />

            <div className="flex-1">
              <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                <div>
                  <p className="font-medium text-white">
                    {getProposedValue(proposal)}
                  </p>

                  {(proposal.proposal_type === "HARD_SKILL" ||
                    proposal.proposal_type === "SOFT_SKILL" ||
                    proposal.proposal_type === "SKILL") && (
                    <div className="mt-3">
                      <label className="block text-xs text-slate-400">
                        Classification detected
                      </label>

                      <select
                        value={
                          skillClassifications[proposal.id] ??
                          (proposal.proposal_type === "SOFT_SKILL"
                            ? "SOFT_SKILL"
                            : "HARD_SKILL")
                        }
                        onChange={(event) =>
                          onSkillClassificationChange(
                            proposal.id,
                            event.target.value as "HARD_SKILL" | "SOFT_SKILL",
                          )
                        }
                        className="mt-1 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-200">
                        <option value="HARD_SKILL">Hard Skill</option>

                        <option value="SOFT_SKILL">Soft Skill</option>
                      </select>
                    </div>
                  )}

                  {proposal.proposal_type === "SKILL" &&
                    proposal.reference_id === null && (
                      <div className="mt-3 space-y-2">
                        <div className="text-xs text-amber-400">
                          Not present in skill catalog
                        </div>

                        <label className="block text-xs text-slate-400">
                          Map to existing skill
                        </label>

                        <input
                          type="search"
                          list={`skill-catalog-${proposal.id}`}
                          placeholder="Search existing skill"
                          className="w-full rounded-md border border-slate-700 bg-slate-950 p-2 text-sm text-slate-200"
                          onChange={(event) => {
                            const selectedSkill = skillsCatalog.find(
                              (skill) => skill.name === event.target.value,
                            );

                            onSkillMappingChange(
                              proposal.id,
                              selectedSkill?.id ?? null,
                            );
                          }}
                        />

                        <datalist id={`skill-catalog-${proposal.id}`}>
                          {skillsCatalog.map((skill) => (
                            <option key={skill.id} value={skill.name} />
                          ))}
                        </datalist>
                      </div>
                    )}
                  <p className="mt-1 text-xs text-slate-500">
                    Source: {proposal.source_field}
                  </p>
                </div>

                {proposal.conflict_detected && (
                  <span className="w-fit rounded bg-amber-950 px-2 py-1 text-xs font-semibold text-amber-300">
                    Conflict
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function renderExperienceList(
  proposals: ProfileEnrichmentProposal[],
  selectedProposalIds: number[],
  editedExperienceValues: Record<number, string>,
  onToggle: (proposalId: number) => void,
  onChange: (proposalId: number, value: string) => void,
) {
  if (proposals.length === 0) {
    return renderEmptyState("Work Experience");
  }

  return (
    <div className="space-y-3">
      {proposals.map((proposal) => (
        <div
          key={proposal.id}
          className="rounded-md border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-start gap-3">
            <input
              type="checkbox"
              checked={selectedProposalIds.includes(proposal.id)}
              onChange={() => onToggle(proposal.id)}
              className="mt-1"
            />

            <div className="flex-1">
              <div className="flex flex-col gap-3">
                <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
                  <div>
                    <p className="font-medium text-white">
                      {getProposedValue(proposal)}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Source: {proposal.source_field}
                    </p>
                  </div>

                  {proposal.conflict_detected && (
                    <span className="w-fit rounded bg-amber-950 px-2 py-1 text-xs font-semibold text-amber-300">
                      Conflict
                    </span>
                  )}
                </div>

                <div className="rounded-md border border-slate-800 bg-slate-950 p-3">
                  <p className="text-xs uppercase text-slate-500">
                    Extracted Value
                  </p>

                  <div className="mt-2 rounded-md border border-slate-800 bg-slate-900 p-3 text-sm text-slate-400">
                    {proposal.proposed_value}
                  </div>
                </div>

                <div className="rounded-md border border-slate-800 bg-slate-950 p-3">
                  <p className="text-xs uppercase text-slate-500">
                    Editable Value
                  </p>

                  <textarea
                    value={
                      editedExperienceValues[proposal.id] ??
                      proposal.proposed_value
                    }
                    onChange={(event) =>
                      onChange(proposal.id, event.target.value)
                    }
                    rows={10}
                    className="mt-2 w-full rounded-md border border-slate-700 bg-slate-900 p-3 text-sm text-slate-300"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export function UploadCvWizardStep3({
  proposals,
  selectedProposalIds,
  editedExperienceValues,
  skillsCatalog,
  skillMappings,
  skillClassifications,
  onToggleProposal,
  onExperienceValueChange,
  onSkillMappingChange,
  onSkillClassificationChange,
}: Props) {
  const hardSkillProposals = proposals.filter(
    (proposal) =>
      proposal.proposal_type === "HARD_SKILL" ||
      proposal.proposal_type === "SKILL",
  );

  const softSkillProposals = proposals.filter(
    (proposal) => proposal.proposal_type === "SOFT_SKILL",
  );

  const experienceProposals = filterProposalsByType(proposals, "EXPERIENCE");

  const languageProposals = filterProposalsByType(proposals, "LANGUAGE");

  const certificationProposals = filterProposalsByType(
    proposals,
    "CERTIFICATION",
  );

  const conflictCount = proposals.filter(
    (proposal) => proposal.conflict_detected,
  ).length;

  const selectedCount = selectedProposalIds.length;

  const excludedCount = proposals.length - selectedCount;

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-6">
      <h3 className="text-lg font-semibold text-white">
        Step 3 - Review & Edit
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        Review the detected information before updating the profile.
      </p>

      <div className="mt-6 rounded-md border border-slate-800 bg-slate-900 p-4">
        <h4 className="font-semibold text-white">Import Summary</h4>

        <div className="mt-3 grid gap-2 md:grid-cols-4">
          <p>Total: {proposals.length}</p>
          <p>Selected: {selectedCount}</p>
          <p>Excluded: {excludedCount}</p>
          <p>Conflicts: {conflictCount}</p>
        </div>
      </div>

      <div className="mt-8 space-y-8">
        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Hard Skills ({hardSkillProposals.length})
          </h4>

          {renderSimpleProposalList(
            hardSkillProposals,
            "Hard Skills",
            selectedProposalIds,
            skillsCatalog,
            skillMappings,
            skillClassifications,
            onToggleProposal,
            onSkillClassificationChange,
            onSkillMappingChange,
          )}
        </section>
        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Soft Skills ({softSkillProposals.length})
          </h4>

          {renderSimpleProposalList(
            softSkillProposals,
            "Soft Skills",
            selectedProposalIds,
            skillsCatalog,
            skillMappings,
            skillClassifications,
            onToggleProposal,
            onSkillClassificationChange,
            onSkillMappingChange,
          )}
        </section>

        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Work Experiences ({experienceProposals.length})
          </h4>

          {renderExperienceList(
            experienceProposals,
            selectedProposalIds,
            editedExperienceValues,
            onToggleProposal,
            onExperienceValueChange,
          )}
        </section>

        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Languages ({languageProposals.length})
          </h4>

          {renderSimpleProposalList(
            languageProposals,
            "Languages",
            selectedProposalIds,
            skillsCatalog,
            skillMappings,
            skillClassifications,
            onToggleProposal,
            onSkillClassificationChange,
            onSkillMappingChange,
          )}
        </section>

        <section>
          <h4 className="mb-3 text-lg font-semibold text-white">
            Certifications ({certificationProposals.length})
          </h4>

          {renderSimpleProposalList(
            certificationProposals,
            "Certifications",
            selectedProposalIds,
            skillsCatalog,
            skillMappings,
            skillClassifications,
            onToggleProposal,
            onSkillClassificationChange,
            onSkillMappingChange,
          )}
        </section>
      </div>
    </div>
  );
}
