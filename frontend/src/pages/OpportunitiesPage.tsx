import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AIExplanationCard } from "../components/AIExplanationCard";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import {
  getApplications,
  getJobOffers,
  getMatching,
  getProfileScoresForJobOffer,
  getProfiles,
  getRankedJobOffers,
  createApplication,
  type ProfileOpportunityScore,
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

type RankedJobOffer = {
  job_offer_id: number;
  matching_score: number;
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
  const [matchingScoresByOfferId, setMatchingScoresByOfferId] = useState<
    Record<number, number>
  >({});

  const [profileScores, setProfileScores] = useState<ProfileOpportunityScore[]>(
    [],
  );

  const [profileScoresLoading, setProfileScoresLoading] = useState(false);
  const [applications, setApplications] = useState<ApplicationSummary[]>([]);
  const [profiles, setProfiles] = useState<any[]>([]);

  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(
    null,
  );

  const [creatingApplication, setCreatingApplication] = useState(false);

  const [searchTerm, setSearchTerm] = useState("");

  const [applicationFilter, setApplicationFilter] = useState<
    "ALL" | "NOT_APPLIED" | "APPLIED"
  >("ALL");

  const [sourceFilter, setSourceFilter] = useState("ALL");
  const [locationFilter, setLocationFilter] = useState("ALL");
  const [sortBy, setSortBy] = useState("BEST_MATCH_FIRST");

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
      if (!selectedOffer || selectedProfileId === null) {
        setMatching(null);
        return;
      }

      setMatchingLoading(true);

      try {
        const result = await getMatching(selectedProfileId, selectedOffer.id);

        setMatching(result);
      } catch {
        setMatching(null);
      } finally {
        setMatchingLoading(false);
      }
    }

    loadMatching();
  }, [selectedOffer, selectedProfileId]);

  useEffect(() => {
    async function loadProfileScores() {
      if (!selectedOffer) {
        setProfileScores([]);
        return;
      }

      setProfileScoresLoading(true);

      try {
        const scores = await getProfileScoresForJobOffer(selectedOffer.id);

        setProfileScores(scores);
      } catch {
        setProfileScores([]);
      } finally {
        setProfileScoresLoading(false);
      }
    }

    loadProfileScores();
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

  useEffect(() => {
    async function loadRankedScores() {
      if (selectedProfileId === null) {
        setMatchingScoresByOfferId({});
        return;
      }

      try {
        const rankedOffers = await getRankedJobOffers(selectedProfileId);

        const scoreMap: Record<number, number> = {};

        (rankedOffers as RankedJobOffer[]).forEach((rankedOffer) => {
          scoreMap[rankedOffer.job_offer_id] = rankedOffer.matching_score;
        });

        setMatchingScoresByOfferId(scoreMap);
      } catch {
        setMatchingScoresByOfferId({});
      }
    }

    loadRankedScores();
  }, [selectedProfileId]);

  function hasApplications(jobOfferId: number) {
    return applications.some(
      (application) => application.job_offer_id === jobOfferId,
    );
  }

  const availableSources = [
    "ALL",
    ...new Set(
      offers
        .map((offer) => offer.source)
        .filter((source): source is string => source !== null),
    ),
  ];

  const availableLocations = [
    "ALL",
    ...new Set(
      offers
        .map((offer) => offer.location)
        .filter((location): location is string => location !== null),
    ),
  ];

  const filteredOffers = offers.filter((offer) => {
    const search = searchTerm.toLowerCase().trim();

    const matchesSearch =
      !search ||
      offer.title?.toLowerCase().includes(search) ||
      offer.company_name?.toLowerCase().includes(search) ||
      offer.location?.toLowerCase().includes(search) ||
      offer.description?.toLowerCase().includes(search);

    const applied = hasApplications(offer.id);

    const matchesApplicationStatus =
      applicationFilter === "ALL"
        ? true
        : applicationFilter === "APPLIED"
          ? applied
          : !applied;

    const matchesSource =
      sourceFilter === "ALL" ? true : offer.source === sourceFilter;

    const matchesLocation =
      locationFilter === "ALL" ? true : offer.location === locationFilter;

    return (
      matchesSearch &&
      matchesApplicationStatus &&
      matchesSource &&
      matchesLocation
    );
  });

  const sortedOffers = [...filteredOffers].sort((a, b) => {
    switch (sortBy) {
      case "BEST_MATCH_FIRST": {
        const aScore = matchingScoresByOfferId[a.id] ?? 0;
        const bScore = matchingScoresByOfferId[b.id] ?? 0;

        return bScore - aScore;
      }
      case "NOT_APPLIED_FIRST": {
        const aApplied = hasApplications(a.id);
        const bApplied = hasApplications(b.id);

        if (aApplied === bApplied) {
          return 0;
        }

        return aApplied ? 1 : -1;
      }

      case "APPLIED_FIRST": {
        const aApplied = hasApplications(a.id);
        const bApplied = hasApplications(b.id);

        if (aApplied === bApplied) {
          return 0;
        }

        return aApplied ? -1 : 1;
      }

      case "NEWEST_FIRST":
        return (
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );

      case "OLDEST_FIRST":
        return (
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        );

      default:
        return 0;
    }
  });

  const totalOpportunities = offers.length;

  const searchSummary = (() => {
    if (searchTerm.trim()) {
      return `Showing ${filteredOffers.length} results for "${searchTerm.trim()}"`;
    }

    if (applicationFilter === "APPLIED") {
      return `Showing ${filteredOffers.length} applied opportunities`;
    }

    if (applicationFilter === "NOT_APPLIED") {
      return `Showing ${filteredOffers.length} not applied opportunities`;
    }

    if (sourceFilter !== "ALL") {
      return `Showing ${filteredOffers.length} opportunities from ${sourceFilter}`;
    }

    if (locationFilter !== "ALL") {
      return `Showing ${filteredOffers.length} opportunities in ${locationFilter}`;
    }

    return "Showing all opportunities";
  })();

  const hasActiveFilters =
    searchTerm.trim() !== "" ||
    applicationFilter !== "ALL" ||
    sourceFilter !== "ALL" ||
    locationFilter !== "ALL";

  const relatedApplications =
    selectedOffer === null
      ? []
      : applications.filter(
          (application) => application.job_offer_id === selectedOffer.id,
        );

  const hasRelatedApplications = relatedApplications.length > 0;

  const bestProfileScore =
    profileScores.find((score) => score.is_best_match) ?? null;

  function getGapFromBest(score: number) {
    if (!bestProfileScore) {
      return 0;
    }

    return Math.round(bestProfileScore.matching_score - score);
  }

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

  function handlePrimaryAction() {
    if (hasRelatedApplications && relatedApplications.length > 0) {
      navigate("/applications", {
        state: {
          applicationId: relatedApplications[0].id,
        },
      });

      return;
    }

    handleCreateApplication();
  }

  return (
    <>
      <PageHeader
        title="Opportunities"
        description="Explore and analyze opportunities."
      />
      <div className="mb-6 flex items-center gap-3">
        <input
          type="text"
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
          placeholder="Search opportunities..."
          className="flex-1 rounded-md border border-slate-700 bg-slate-950 px-4 py-2 text-white outline-none focus:border-blue-500"
        />

        {hasActiveFilters && (
          <button
            type="button"
            onClick={() => {
              setSearchTerm("");
              setApplicationFilter("ALL");
              setSourceFilter("ALL");
              setSortBy("BEST_MATCH_FIRST");
              setLocationFilter("ALL");
            }}
            className="rounded-md border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800">
            Reset
          </button>
        )}
      </div>

      <div className="mb-4 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <div className="flex flex-wrap items-center gap-3">
          <div>
            <p className="text-sm font-medium text-white">
              Opportunity Context
            </p>

            <p className="text-xs text-slate-400">
              Active profile used for opportunity ranking and matching analysis.
            </p>
          </div>

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
        </div>
      </div>
      <div className="mb-4 flex items-center gap-2">
        <button
          type="button"
          onClick={() => setApplicationFilter("ALL")}
          className={`rounded-md px-3 py-2 text-sm ${
            applicationFilter === "ALL"
              ? "bg-blue-600 text-white"
              : "border border-slate-700 text-slate-300"
          }`}>
          All
        </button>

        <button
          type="button"
          onClick={() => setApplicationFilter("NOT_APPLIED")}
          className={`rounded-md px-3 py-2 text-sm ${
            applicationFilter === "NOT_APPLIED"
              ? "bg-blue-600 text-white"
              : "border border-slate-700 text-slate-300"
          }`}>
          Not Applied
        </button>

        <button
          type="button"
          onClick={() => setApplicationFilter("APPLIED")}
          className={`rounded-md px-3 py-2 text-sm ${
            applicationFilter === "APPLIED"
              ? "bg-blue-600 text-white"
              : "border border-slate-700 text-slate-300"
          }`}>
          Applied
        </button>

        <select
          value={locationFilter}
          onChange={(event) => setLocationFilter(event.target.value)}
          className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white">
          {availableLocations.map((location) => (
            <option key={location} value={location}>
              {location === "ALL" ? "All Locations" : location}
            </option>
          ))}
        </select>

        <select
          value={sourceFilter}
          onChange={(event) => setSourceFilter(event.target.value)}
          className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white">
          {availableSources.map((source) => (
            <option key={source} value={source}>
              {source === "ALL" ? "All Sources" : source}
            </option>
          ))}
        </select>
        <select
          value={sortBy}
          onChange={(event) => setSortBy(event.target.value)}
          className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white">
          <option value="BEST_MATCH_FIRST">Best Match First</option>
          <option value="NOT_APPLIED_FIRST">Not Applied First</option>

          <option value="APPLIED_FIRST">Applied First</option>

          <option value="NEWEST_FIRST">Newest First</option>

          <option value="OLDEST_FIRST">Oldest First</option>
        </select>
      </div>

      <div className="mb-6 text-sm text-slate-400">
        <p>{totalOpportunities} total opportunities</p>

        <p>{searchSummary}</p>
      </div>

      {loading && <p className="text-slate-400">Loading opportunities...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="max-h-[calc(100vh-220px)] space-y-3 overflow-y-auto pr-2">
            {filteredOffers.length === 0 ? (
              <Card>
                <p className="text-slate-400">
                  No opportunities match your search.
                </p>
              </Card>
            ) : (
              sortedOffers.map((offer) => (
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
                    <div className="mb-2 flex items-center gap-2">
                      {hasApplications(offer.id) ? (
                        <span className="rounded bg-green-600 px-2 py-1 text-xs text-white">
                          Applied
                        </span>
                      ) : (
                        <span className="rounded bg-amber-600 px-2 py-1 text-xs text-white">
                          Not Applied
                        </span>
                      )}

                      {matchingScoresByOfferId[offer.id] !== undefined && (
                        <span className="rounded bg-blue-600 px-2 py-1 text-xs font-medium text-white">
                          ⭐ Match{" "}
                          {Math.round(matchingScoresByOfferId[offer.id])}%
                        </span>
                      )}
                    </div>

                    <h3 className="font-medium text-white">{offer.title}</h3>

                    <p className="text-sm text-slate-300">
                      {offer.company_name ?? "Unknown company"}
                    </p>

                    <p className="text-xs text-slate-500">{offer.location}</p>
                  </Card>
                </button>
              ))
            )}
          </div>

          <div className="sticky top-6 self-start lg:col-span-2">
            {selectedOffer ? (
              <Card>
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-3xl font-bold text-white">
                    {selectedOffer.title}
                  </h2>

                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      disabled={creatingApplication}
                      onClick={handlePrimaryAction}
                      className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500">
                      {creatingApplication
                        ? "Creating..."
                        : hasRelatedApplications
                          ? "Open Application"
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

                <div className="mb-8 border-t border-slate-700 pt-6">
                  <div className="mb-4 flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-white">
                        Profile Scores
                      </h3>

                      <p className="text-xs text-slate-400">
                        Compare how this opportunity matches each available
                        profile.
                      </p>
                    </div>

                    <span className="text-xs text-slate-400">
                      {profileScores.length} profiles evaluated
                    </span>
                  </div>

                  {profileScoresLoading ? (
                    <p className="text-slate-400">Loading profile scores...</p>
                  ) : profileScores.length === 0 ? (
                    <p className="text-slate-400">
                      No profile scores available.
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {bestProfileScore && (
                        <div className="rounded-lg border border-blue-500 bg-blue-500/10 p-4">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-xs font-medium uppercase tracking-wide text-blue-300">
                                Best Matching Profile
                              </p>

                              <p className="mt-1 text-base font-semibold text-white">
                                🥇 {bestProfileScore.profile_name}
                              </p>
                            </div>

                            <p className="text-2xl font-bold text-white">
                              {Math.round(bestProfileScore.matching_score)}%
                            </p>
                          </div>
                        </div>
                      )}

                      <div className="max-h-56 overflow-y-auto rounded-lg border border-slate-700">
                        <table className="w-full text-sm">
                          <thead className="sticky top-0 bg-slate-900 text-left text-xs uppercase tracking-wide text-slate-400">
                            <tr>
                              <th className="px-4 py-3">Profile</th>

                              <th className="px-4 py-3 text-right">Score</th>

                              <th className="px-4 py-3 text-right">Skills</th>

                              <th className="px-4 py-3 text-right">
                                Experience
                              </th>

                              <th className="px-4 py-3 text-right">
                                Work Mode
                              </th>

                              <th className="px-4 py-3 text-right">Location</th>
                            </tr>
                          </thead>

                          <tbody>
                            {profileScores
                              .filter((score) => !score.is_best_match)
                              .map((score) => (
                                <tr
                                  key={score.profile_id}
                                  className={
                                    score.is_best_match
                                      ? "border-t border-blue-500/40 bg-blue-500/10"
                                      : "border-t border-slate-800"
                                  }>
                                  <td className="px-4 py-3">
                                    <div className="flex flex-col">
                                      <span className="font-medium text-white">
                                        {score.profile_name}
                                      </span>

                                      {score.is_best_match && (
                                        <span className="mt-1 w-fit rounded-full bg-blue-600/30 px-2 py-0.5 text-xs text-blue-200">
                                          🥇 Best Match
                                        </span>
                                      )}
                                    </div>
                                  </td>

                                  <td className="px-4 py-3 text-right">
                                    <div className="flex flex-col items-end">
                                      <span className="font-semibold text-white">
                                        {Math.round(score.matching_score)}%
                                      </span>

                                      <span className="text-xs text-slate-500">
                                        -{getGapFromBest(score.matching_score)}{" "}
                                        pts
                                      </span>
                                    </div>
                                  </td>

                                  <td className="px-4 py-3 text-right text-slate-300">
                                    {Math.round(score.skills_score)}%
                                  </td>

                                  <td className="px-4 py-3 text-right text-slate-300">
                                    {Math.round(score.experience_score)}%
                                  </td>

                                  <td className="px-4 py-3 text-right text-slate-300">
                                    {Math.round(score.work_mode_score)}%
                                  </td>

                                  <td className="px-4 py-3 text-right text-slate-300">
                                    {Math.round(score.location_score)}%
                                  </td>
                                </tr>
                              ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>

                <div className="border-t border-slate-700 pt-6">
                  <div className="mb-4 flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-white">
                      Matching Analysis
                    </h3>

                    <span className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-300">
                      Active Profile:{" "}
                      {profiles.find(
                        (profile) => profile.id === selectedProfileId,
                      )?.full_name ?? "Unknown"}
                    </span>
                  </div>

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
