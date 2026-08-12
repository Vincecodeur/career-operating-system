import { useState } from "react";

import type { ProfileEnrichmentProposal } from "../../services/api";

type ReviewSection = "skills" | "experiences" | "languages" | "certifications";

type Props = {
  proposals: ProfileEnrichmentProposal[];
};

type SectionConfig = {
  id: ReviewSection;
  label: string;
  description: string;
};

const sections: SectionConfig[] = [
  {
    id: "skills",
    label: "Skills",
    description: "Skills detected in the CV.",
  },
  {
    id: "experiences",
    label: "Work Experience",
    description: "Professional experiences detected in the CV.",
  },
  {
    id: "languages",
    label: "Languages",
    description: "Languages detected in the CV.",
  },
  {
    id: "certifications",
    label: "Certifications",
    description: "Certifications detected in the CV.",
  },
];

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
        </div>
      ))}
    </div>
  );
}

function renderExperienceList(
  proposals: ProfileEnrichmentProposal[],
  expandedExperienceIds: number[],
  onToggleExperience: (proposalId: number) => void,
) {
  if (proposals.length === 0) {
    return renderEmptyState("Work Experience");
  }

  return (
    <div className="space-y-3">
      {proposals.map((proposal) => {
        const isExpanded = expandedExperienceIds.includes(proposal.id);

        return (
          <div
            key={proposal.id}
            className="rounded-md border border-slate-800 bg-slate-900 p-4">
            <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
              <div>
                <p className="font-medium text-white">
                  {getProposedValue(proposal)}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  Source: {proposal.source_field}
                </p>
              </div>

              <div className="flex items-center gap-2">
                {proposal.conflict_detected && (
                  <span className="rounded bg-amber-950 px-2 py-1 text-xs font-semibold text-amber-300">
                    Conflict
                  </span>
                )}

                <button
                  type="button"
                  onClick={() => onToggleExperience(proposal.id)}
                  className="rounded-md border border-slate-600 px-3 py-1 text-sm text-slate-300 hover:bg-slate-800">
                  {isExpanded ? "Hide" : "Review"}
                </button>
              </div>
            </div>

            {isExpanded && (
              <div className="mt-4 rounded-md border border-slate-800 bg-slate-950 p-4">
                <div className="space-y-3">
                  <div>
                    <p className="text-xs uppercase text-slate-500">
                      Proposed Value
                    </p>

                    <p className="mt-1 whitespace-pre-wrap text-sm text-slate-300">
                      {proposal.proposed_value}
                    </p>
                  </div>

                  <div>
                    <p className="text-xs uppercase text-slate-500">
                      Observed Value
                    </p>

                    <p className="mt-1 whitespace-pre-wrap text-sm text-slate-400">
                      {proposal.observed_value}
                    </p>
                  </div>

                  {proposal.current_profile_value && (
                    <div>
                      <p className="text-xs uppercase text-slate-500">
                        Current Profile Value
                      </p>

                      <p className="mt-1 whitespace-pre-wrap text-sm text-slate-400">
                        {proposal.current_profile_value}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export function UploadCvWizardStep3({ proposals }: Props) {
  const [activeSection, setActiveSection] = useState<ReviewSection>("skills");

  const [expandedExperienceIds, setExpandedExperienceIds] = useState<number[]>(
    [],
  );

  const skillProposals = filterProposalsByType(proposals, "SKILL");

  const experienceProposals = filterProposalsByType(proposals, "EXPERIENCE");

  const languageProposals = filterProposalsByType(proposals, "LANGUAGE");

  const certificationProposals = filterProposalsByType(
    proposals,
    "CERTIFICATION",
  );

  const conflictCount = proposals.filter(
    (proposal) => proposal.conflict_detected,
  ).length;

  function toggleExperience(proposalId: number) {
    setExpandedExperienceIds((currentIds) => {
      if (currentIds.includes(proposalId)) {
        return currentIds.filter((currentId) => currentId !== proposalId);
      }

      return [...currentIds, proposalId];
    });
  }

  function renderActiveSection() {
    if (activeSection === "skills") {
      return renderSimpleProposalList(skillProposals, "Skills");
    }

    if (activeSection === "experiences") {
      return renderExperienceList(
        experienceProposals,
        expandedExperienceIds,
        toggleExperience,
      );
    }

    if (activeSection === "languages") {
      return renderSimpleProposalList(languageProposals, "Languages");
    }

    return renderSimpleProposalList(certificationProposals, "Certifications");
  }

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-950 p-6">
      <div>
        <h3 className="text-lg font-semibold text-white">
          Step 3 - Review & Edit
        </h3>

        <p className="mt-2 text-sm text-slate-400">
          Review the detected information before updating the profile.
        </p>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-[180px_1fr]">
        <div className="space-y-2">
          {sections.map((section) => (
            <button
              key={section.id}
              type="button"
              onClick={() => setActiveSection(section.id)}
              className={[
                "w-full rounded-md border px-3 py-2 text-left text-sm",
                activeSection === section.id
                  ? "border-blue-600 bg-blue-950 text-blue-200"
                  : "border-slate-800 bg-slate-900 text-slate-400 hover:bg-slate-800",
              ].join(" ")}>
              {section.label}
            </button>
          ))}

          <div className="rounded-md border border-slate-800 bg-slate-900 p-3">
            <p className="text-xs uppercase text-slate-500">Import Summary</p>

            <div className="mt-3 space-y-1 text-sm text-slate-300">
              <p>Skills: {skillProposals.length}</p>

              <p>Experiences: {experienceProposals.length}</p>

              <p>Languages: {languageProposals.length}</p>

              <p>Certifications: {certificationProposals.length}</p>

              <p>Conflicts: {conflictCount}</p>
            </div>
          </div>
        </div>

        <div>
          <div className="mb-4">
            <h4 className="font-semibold text-white">
              {sections.find((section) => section.id === activeSection)?.label}
            </h4>

            <p className="mt-1 text-sm text-slate-400">
              {
                sections.find((section) => section.id === activeSection)
                  ?.description
              }
            </p>
          </div>

          {renderActiveSection()}
        </div>
      </div>
    </div>
  );
}
