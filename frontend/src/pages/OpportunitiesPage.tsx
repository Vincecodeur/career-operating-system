import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AIExplanationCard } from "../components/AIExplanationCard";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import {
  getApplications,
  getJobOffers,
  getMatching,
  getProfiles,
  createApplication,
} from "../services/api";
import { MatchingResult } from "../components/MatchingResult";

type JobOffer = {
  id: number;
  title: string;
  company_name: string | null;
  location: string | null;
  source: string | null;
  source_url: string | null;
  description: string | null;
  created_at: string;
};

type ScoreExplanation = {
  criterion: string;
  score: number;
  message: string;
};

type OpportunityAnalysis = {
  verdict: string;
  recommendation: string;
  summary: string;
};

type AIExplanation = {
  summary: string;
  detailed_explanation: string;
  action_plan: string[];
  provider_name: string;
  model_name: string;
  prompt_version: string;
};

type MatchingData = {
  matching_score: number;
  skills_score: number;
  experience_score: number;
  work_mode_score: number;
  location_score: number;
  matching_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
  opportunity_analysis: OpportunityAnalysis;
  explanations: ScoreExplanation[];
  ai_explanation?: AIExplanation | null;
};

type ApplicationSummary = {
  id: number;
  profile_id: number;
  job_offer_id: number;
  status: string;
  source_type: string;
};

export function OpportunitiesPage() {
  const [offers, setOffers] = useState<JobOffer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<JobOffer | null>(null);
  const [matching, setMatching] = useState<MatchingData | null>(null);
  const [applications, setApplications] = useState<ApplicationSummary[]>([]);
  const [profiles, setProfiles] = useState<any[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(
    null,
  );

  const [creatingApplication, setCreatingApplication] = useState(false);

  const [loading, setLoading] = useState(true);
  const [matchingLoading, setMatchingLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();

  const selectedJobOfferId = (location.state as { jobOfferId?: number } | null)
    ?.jobOfferId;

  useEffect(() => {
    async function loadOffers() {
      try {
        const data = await getJobOffers();

        setOffers(data);

        if (data.length > 0) {
          const preselectedOffer =
            selectedJobOfferId !== undefined
              ? data.find((offer: JobOffer) => offer.id === selectedJobOfferId)
              : null;

          setSelectedOffer(preselectedOffer ?? data[0]);
        }
      } catch {
        setError("Unable to load opportunities.");
      } finally {
        setLoading(false);
      }
    }

    loadOffers();
  }, [selectedJobOfferId]);

  useEffect(() => {
    async function loadApplications() {
      try {
        const data = await getApplications();

        const applicationList = Array.isArray(data) ? data : (data.value ?? []);

        setApplications(applicationList);
      } catch {
        setApplications([]);
      }
    }

    loadApplications();
  }, []);

  useEffect(() => {
    async function loadMatching() {
      if (!selectedOffer) {
        return;
      }

      setMatchingLoading(true);

      try {
        const result = await getMatching(1, selectedOffer.id);

        setMatching(result);
      } catch {
        setMatching(null);
      } finally {
        setMatchingLoading(false);
      }
    }

    loadMatching();
  }, [selectedOffer]);

  useEffect(() => {
    async function loadProfiles() {
      try {
        const data = await getProfiles();

        const profileList = Array.isArray(data) ? data : (data.value ?? []);

        setProfiles(profileList);

        if (profileList.length > 0) {
          setSelectedProfileId(profileList[0].id);
        }
      } catch {
        setProfiles([]);
      }
    }

    loadProfiles();
  }, []);

  const relatedApplications =
    selectedOffer === null
      ? []
      : applications.filter(
          (application) => application.job_offer_id === selectedOffer.id,
        );

  async function handleCreateApplication() {
    if (!selectedOffer || selectedProfileId === null) {
      return;
    }

    setCreatingApplication(true);

    try {
      await createApplication({
        profile_id: selectedProfileId,
        job_offer_id: selectedOffer.id,
        status: "Applied",
        notes: null,
        source_type: "OPPORTUNITY",
      });

      const refreshedApplications = await getApplications();

      setApplications(
        Array.isArray(refreshedApplications)
          ? refreshedApplications
          : (refreshedApplications.value ?? []),
      );
    } finally {
      setCreatingApplication(false);
    }
  }

  return (
    <>
      <PageHeader
        title="Opportunities"
        description="Explore and analyze opportunities."
      />

      <p className="mb-6 text-sm text-slate-400">
        {offers.length} opportunities found
      </p>

      {loading && <p className="text-slate-400">Loading opportunities...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="max-h-[calc(100vh-220px)] space-y-3 overflow-y-auto pr-2">
            {offers.map((offer) => (
              <button
                key={offer.id}
                type="button"
                onClick={() => setSelectedOffer(offer)}
                className={`block w-full rounded-lg text-left transition-all ${
                  selectedOffer?.id === offer.id
                    ? "border-2 border-blue-500 bg-slate-800 shadow-lg shadow-blue-500/20"
                    : ""
                }`}>
                <Card>
                  <h3 className="font-medium text-white">{offer.title}</h3>

                  <p className="text-sm text-slate-300">
                    {offer.company_name ?? "Unknown company"}
                  </p>

                  <p className="text-xs text-slate-500">{offer.location}</p>
                </Card>
              </button>
            ))}
          </div>

          <div className="sticky top-6 self-start lg:col-span-2">
            {selectedOffer ? (
              <Card>
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-3xl font-bold text-white">
                    {selectedOffer.title}
                  </h2>

                  <div className="flex items-center gap-3">
                    <select
                      value={selectedProfileId ?? ""}
                      onChange={(event) =>
                        setSelectedProfileId(Number(event.target.value))
                      }
                      className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white">
                      {profiles.map((profile) => (
                        <option key={profile.id} value={profile.id}>
                          {profile.full_name}
                        </option>
                      ))}
                    </select>

                    <button
                      type="button"
                      disabled={creatingApplication}
                      onClick={handleCreateApplication}
                      className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500">
                      {creatingApplication
                        ? "Creating..."
                        : "Create Application"}
                    </button>
                  </div>
                </div>

                <div className="mb-8 grid grid-cols-2 gap-4 text-sm text-slate-400">
                  <div>
                    <p className="font-medium text-slate-300">Company</p>

                    <p>{selectedOffer.company_name ?? "Unknown"}</p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">Source</p>

                    <p>{selectedOffer.source ?? "Unknown"}</p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">Location</p>

                    <p>{selectedOffer.location ?? "Unknown"}</p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">Imported</p>

                    <p>{new Date(selectedOffer.created_at).toLocaleString()}</p>
                  </div>
                </div>

                {selectedOffer.source_url && (
                  <div className="mb-8">
                    <a
                      href={selectedOffer.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:text-blue-400">
                      View Original Offer
                    </a>
                  </div>
                )}
                <div className="mb-8 border-t border-slate-700 pt-6">
                  <h3 className="mb-4 text-lg font-semibold text-white">
                    Applications ({relatedApplications.length})
                  </h3>

                  {relatedApplications.length === 0 ? (
                    <p className="text-slate-400">
                      No applications linked to this opportunity.
                    </p>
                  ) : (
                    <div className="space-y-3">
                      {relatedApplications.map((application) => (
                        <div
                          key={application.id}
                          className="rounded-lg border border-slate-700 p-4">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="font-medium text-white">
                                Application #{application.id}
                              </p>

                              <p className="text-sm text-slate-400">
                                Profile {application.profile_id}
                              </p>

                              <p className="text-sm text-slate-400">
                                {application.status}
                              </p>

                              <p className="text-sm text-slate-500">
                                {application.source_type}
                              </p>
                            </div>

                            <button
                              type="button"
                              onClick={() =>
                                navigate("/applications", {
                                  state: {
                                    applicationId: application.id,
                                  },
                                })
                              }
                              className="rounded-md border border-blue-500 px-3 py-1 text-sm text-blue-300 hover:bg-blue-500/10">
                              Open Application
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <div className="mb-8">
                  <h3 className="mb-3 text-lg font-semibold text-white">
                    Description
                  </h3>

                  <p className="whitespace-pre-wrap text-slate-300">
                    {selectedOffer.description ?? "No description available."}
                  </p>
                </div>

                <div className="border-t border-slate-700 pt-6">
                  <h3 className="mb-4 text-lg font-semibold text-white">
                    Matching Analysis
                  </h3>

                  {matching ? (
                    <MatchingResult
                      matchingScore={matching.matching_score}
                      skillsScore={matching.skills_score}
                      experienceScore={matching.experience_score}
                      workModeScore={matching.work_mode_score}
                      locationScore={matching.location_score}
                      matchingSkills={matching.matching_skills}
                      missingSkills={matching.missing_skills}
                      strengths={matching.strengths}
                      weaknesses={matching.weaknesses}
                      explanations={matching.explanations}
                      opportunityAnalysis={matching.opportunity_analysis}
                    />
                  ) : (
                    <p className="text-slate-400">
                      Matching information unavailable.
                    </p>
                  )}
                </div>

                <div className="mt-8 border-t border-slate-700 pt-6">
                  <AIExplanationCard
                    explanation={matching?.ai_explanation ?? null}
                    isLoading={matchingLoading}
                    error={null}
                  />
                </div>

                {selectedOffer.source_url && (
                  <div className="mt-8 border-t border-slate-700 pt-6">
                    <a
                      href={selectedOffer.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:text-blue-400">
                      Open Source Offer
                    </a>
                  </div>
                )}
              </Card>
            ) : (
              <Card>
                <p className="text-slate-400">
                  Select an opportunity to view details.
                </p>
              </Card>
            )}
          </div>
        </div>
      )}
    </>
  );
}
