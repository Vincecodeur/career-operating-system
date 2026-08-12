import { useEffect, useState } from "react";

import { UploadCvWizardStep1 } from "./cv-wizard/UploadCvWizardStep1";
import { UploadCvWizardStep2 } from "./cv-wizard/UploadCvWizardStep2";
import { UploadCvWizardStep3 } from "./cv-wizard/UploadCvWizardStep3";
import { WizardProgress } from "./cv-wizard/WizardProgress";

import type { Cv, ProfileEnrichmentProposal } from "../services/api";
import { generateProfileEnrichment } from "../services/api";

export type UploadCvFormValues = {
  file: File;
  language: string;
  versionLabel: string;
  isDefault: boolean;
};

type WizardStep = "upload" | "analysis" | "review" | "summary";

type Props = {
  isOpen: boolean;
  isSaving: boolean;
  error: string | null;
  onClose: () => void;
  onUpload: (values: UploadCvFormValues) => Promise<Cv>;
};

function countProposalsByType(
  proposals: ProfileEnrichmentProposal[],
  proposalType: string,
) {
  return proposals.filter((proposal) => proposal.proposal_type === proposalType)
    .length;
}

function countConflicts(proposals: ProfileEnrichmentProposal[]) {
  return proposals.filter((proposal) => proposal.conflict_detected).length;
}

export function UploadCvModal({
  isOpen,
  isSaving,
  error,
  onClose,
  onUpload,
}: Props) {
  const [step, setStep] = useState<WizardStep>("upload");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [language, setLanguage] = useState("");
  const [versionLabel, setVersionLabel] = useState("");
  const [isDefault, setIsDefault] = useState(false);

  const [localError, setLocalError] = useState<string | null>(null);

  const [enrichmentProposals, setEnrichmentProposals] = useState<
    ProfileEnrichmentProposal[]
  >([]);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    setStep("upload");
    setSelectedFile(null);
    setLanguage("");
    setVersionLabel("");
    setIsDefault(false);
    setLocalError(null);
    setEnrichmentProposals([]);
    setIsAnalyzing(false);
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setLocalError("Please select a CV file.");
      return;
    }

    setLocalError(null);
    setIsAnalyzing(true);

    let uploadedCv: Cv;

    try {
      uploadedCv = await onUpload({
        file: selectedFile,
        language,
        versionLabel,
        isDefault,
      });
    } catch {
      setLocalError("Unable to upload CV.");
      setIsAnalyzing(false);
      return;
    }

    try {
      const proposals = await generateProfileEnrichment(uploadedCv.id);

      console.log("ENRICHMENT_PROPOSALS", proposals);

      setEnrichmentProposals(proposals);
      setStep("analysis");
    } catch {
      setLocalError("CV uploaded, but analysis could not be completed.");
    } finally {
      setIsAnalyzing(false);
    }
  }

  const skillsFound = countProposalsByType(enrichmentProposals, "SKILL");

  const experiencesFound = countProposalsByType(
    enrichmentProposals,
    "EXPERIENCE",
  );

  const languagesFound = countProposalsByType(enrichmentProposals, "LANGUAGE");

  const certificationsFound = countProposalsByType(
    enrichmentProposals,
    "CERTIFICATION",
  );

  const conflictCount = countConflicts(enrichmentProposals);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-5xl max-h-[90vh] rounded-lg border border-slate-700 bg-slate-900 shadow-xl flex flex-col">
        <div className="flex-1 overflow-y-auto p-6">
          <h2 className="text-2xl font-bold text-white">
            Update Profile From CV
          </h2>

          <p className="mt-2 text-sm text-slate-400">
            Upload a CV and start the profile enrichment workflow.
          </p>

          <WizardProgress currentStep={step} />

          {(error || localError) && (
            <div className="mb-4 rounded-md border border-red-800 bg-red-950 p-3 text-sm text-red-300">
              {localError ?? error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {step === "upload" && (
              <UploadCvWizardStep1
                selectedFile={selectedFile}
                language={language}
                versionLabel={versionLabel}
                isDefault={isDefault}
                isSaving={isSaving || isAnalyzing}
                onFileChange={setSelectedFile}
                onLanguageChange={setLanguage}
                onVersionLabelChange={setVersionLabel}
                onIsDefaultChange={setIsDefault}
              />
            )}

            {step === "analysis" && (
              <UploadCvWizardStep2
                skillsFound={skillsFound}
                experiencesFound={experiencesFound}
                languagesFound={languagesFound}
                certificationsFound={certificationsFound}
                conflictCount={conflictCount}
              />
            )}

            {step === "review" && (
              <UploadCvWizardStep3 proposals={enrichmentProposals} />
            )}

            <div className="flex justify-end gap-3 border-t border-slate-700 pt-5">
              <button
                type="button"
                onClick={onClose}
                disabled={isSaving || isAnalyzing}
                className="rounded-md border border-slate-600 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 disabled:opacity-50">
                {step === "upload" ? "Cancel" : "Close"}
              </button>

              {step === "analysis" && (
                <button
                  type="button"
                  onClick={() => setStep("review")}
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500">
                  Review Suggestions
                </button>
              )}

              {step === "upload" && (
                <button
                  type="submit"
                  disabled={isSaving || isAnalyzing}
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
                  {isAnalyzing
                    ? "Analyzing..."
                    : isSaving
                      ? "Uploading..."
                      : "Upload and Analyze"}
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
