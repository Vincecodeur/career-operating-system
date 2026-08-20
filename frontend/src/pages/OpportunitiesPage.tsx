import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AIExplanationCard } from "../components/AIExplanationCard";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import {
  createApplication,
  createSavedSearch,
  deleteSavedSearch,
  getApplications,
  getDiscoveryPreferencesSettings,
  getJobOffers,
  getMatching,
  getProfileScoresForJobOffer,
  getProfiles,
  getRankedJobOffers,
  getSavedSearches,
  type DiscoveryPreferencesSettings,
  type Profile,
  type ProfileOpportunityScore,
  type SavedSearch,
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
  const [profiles, setProfiles] = useState<Profile[]>([]);

  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(
    null,
  );

  const [activeProfileIds, setActiveProfileIds] = useState<number[]>([]);

  const [creatingApplication, setCreatingApplication] = useState(false);

  const [isCreateApplicationModalOpen, setIsCreateApplicationModalOpen] =
    useState(false);

  const [applicationProfileId, setApplicationProfileId] = useState<
    number | null
  >(null);

  const [applicationCreationError, setApplicationCreationError] = useState<
    string | null
  >(null);

  const [searchTerm, setSearchTerm] = useState("");

  const [applicationFilter, setApplicationFilter] = useState<
    "ALL" | "NOT_APPLIED" | "APPLIED"
  >("ALL");

  const [sourceFilter, setSourceFilter] = useState("ALL");
  const [locationFilter, setLocationFilter] = useState("ALL");
  const [sortBy, setSortBy] = useState("BEST_MATCH_FIRST");
  const [discoveryPreferences, setDiscoveryPreferences] =
    useState<DiscoveryPreferencesSettings | null>(null);

  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([]);
  const [savedSearchName, setSavedSearchName] = useState("");
  const [showSaveSearchForm, setShowSaveSearchForm] = useState(false);
  const [savingSearch, setSavingSearch] = useState(false);
  const [savedSearchError, setSavedSearchError] = useState<string | null>(null);

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
    async function loadDiscoveryPreferences() {
      try {
        const preferences = await getDiscoveryPreferencesSettings();

        setDiscoveryPreferences(preferences);

        setSortBy(preferences.discovery_default_sort);
      } catch {
        setDiscoveryPreferences(null);
      }
    }

    loadDiscoveryPreferences();
  }, []);

  useEffect(() => {
    async function loadSavedSearches() {
      try {
        const data = await getSavedSearches();

        setSavedSearches(data);
      } catch {
        setSavedSearches([]);
      }
    }

    loadSavedSearches();
  }, []);

  useEffect(() => {
    async function loadProfiles() {
      try {
        const data = await getProfiles();

        const profileList = Array.isArray(data) ? data : (data.value ?? []);

        const availableProfiles = profileList.filter(
          (profile: Profile) => profile.is_active,
        );

        setProfiles(availableProfiles);

        if (availableProfiles.length > 0) {
          const firstProfileId = availableProfiles[0].id;

          setSelectedProfileId(firstProfileId);

          setActiveProfileIds([firstProfileId]);
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

  function isActiveProfile(profileId: number) {
    return activeProfileIds.includes(profileId);
  }

  function toggleActiveProfile(profileId: number) {
    if (profileId === selectedProfileId) {
      return;
    }

    setActiveProfileIds((currentProfiles) => {
      const isActive = currentProfiles.includes(profileId);

      if (isActive) {
        return currentProfiles.filter((id) => id !== profileId);
      }

      return [...currentProfiles, profileId];
    });
  }

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

    const minimumScore =
      discoveryPreferences?.discovery_minimum_matching_score ?? 25;

    const offerScore = matchingScoresByOfferId[offer.id] ?? 0;

    const matchesMinimumScore = offerScore >= minimumScore;

    const ageWindow = discoveryPreferences?.discovery_age_window ?? "30_DAYS";

    const now = Date.now();

    const ageLimitDays =
      ageWindow === "7_DAYS"
        ? 7
        : ageWindow === "14_DAYS"
          ? 14
          : ageWindow === "30_DAYS"
            ? 30
            : ageWindow === "90_DAYS"
              ? 90
              : null;

    const matchesAgeWindow =
      ageLimitDays === null
        ? true
        : now - new Date(offer.created_at).getTime() <=
          ageLimitDays * 24 * 60 * 60 * 1000;

    return (
      matchesSearch &&
      matchesApplicationStatus &&
      matchesSource &&
      matchesLocation &&
      matchesMinimumScore &&
      matchesAgeWindow
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

  const activeProfileScores = profileScores.filter((score) =>
    activeProfileIds.includes(score.profile_id),
  );

  const bestProfileScore =
    [...activeProfileScores].sort((firstScore, secondScore) => {
      const scoreDifference =
        secondScore.matching_score - firstScore.matching_score;

      if (scoreDifference !== 0) {
        return scoreDifference;
      }

      if (
        firstScore.profile_id === selectedProfileId &&
        secondScore.profile_id !== selectedProfileId
      ) {
        return -1;
      }

      if (
        secondScore.profile_id === selectedProfileId &&
        firstScore.profile_id !== selectedProfileId
      ) {
        return 1;
      }

      return firstScore.profile_id - secondScore.profile_id;
    })[0] ?? null;

  function getDefaultApplicationProfileId() {
    if (
      bestProfileScore &&
      profiles.some((profile) => profile.id === bestProfileScore.profile_id)
    ) {
      return bestProfileScore.profile_id;
    }

    if (
      selectedProfileId !== null &&
      profiles.some((profile) => profile.id === selectedProfileId)
    ) {
      return selectedProfileId;
    }

    return null;
  }

  function getGapFromBest(score: number) {
    if (!bestProfileScore) {
      return 0;
    }

    return Math.round(bestProfileScore.matching_score - score);
  }

  function openCreateApplicationModal() {
    if (!selectedOffer) {
      return;
    }

    setApplicationProfileId(getDefaultApplicationProfileId());
    setApplicationCreationError(null);
    setIsCreateApplicationModalOpen(true);
  }

  function closeCreateApplicationModal() {
    if (creatingApplication) {
      return;
    }

    setIsCreateApplicationModalOpen(false);
    setApplicationProfileId(null);
    setApplicationCreationError(null);
  }

  async function handleCreateApplication() {
    if (!selectedOffer) {
      setApplicationCreationError("An opportunity is required.");
      return;
    }

    if (applicationProfileId === null) {
      setApplicationCreationError("An application profile is required.");
      return;
    }

    setCreatingApplication(true);
    setApplicationCreationError(null);

    try {
      await createApplication({
        profile_id: applicationProfileId,
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

      setIsCreateApplicationModalOpen(false);
      setApplicationProfileId(null);
    } catch (error) {
      setApplicationCreationError(
        error instanceof Error
          ? error.message
          : "Unable to create application.",
      );
    } finally {
      setCreatingApplication(false);
    }
  }

  async function handleSaveSearch() {
    const cleanName = savedSearchName.trim();

    if (!cleanName) {
      setSavedSearchError("Search name is required.");
      return;
    }

    setSavingSearch(true);
    setSavedSearchError(null);

    try {
      const createdSearch = await createSavedSearch({
        name: cleanName,
        keyword: searchTerm.trim(),
        application_status: applicationFilter,
        source: sourceFilter,
        location: locationFilter,
        sort_by: sortBy,
      });

      setSavedSearches((currentSearches) => [
        ...currentSearches,
        createdSearch,
      ]);

      setSavedSearchName("");
      setShowSaveSearchForm(false);
    } catch {
      setSavedSearchError("Unable to save the current search.");
    } finally {
      setSavingSearch(false);
    }
  }

  function handleApplySavedSearch(savedSearch: SavedSearch) {
    setSearchTerm(savedSearch.keyword);
    setApplicationFilter(savedSearch.application_status);
    setSourceFilter(savedSearch.source);
    setLocationFilter(savedSearch.location);
    setSortBy(savedSearch.sort_by);
    setSavedSearchError(null);
  }

  async function handleDeleteSavedSearch(savedSearchId: number) {
    const confirmed = window.confirm(
      "Delete this saved search? This action cannot be undone.",
    );

    if (!confirmed) {
      return;
    }

    setSavedSearchError(null);

    try {
      await deleteSavedSearch(savedSearchId);

      setSavedSearches((currentSearches) =>
        currentSearches.filter(
          (savedSearch) => savedSearch.id !== savedSearchId,
        ),
      );
    } catch {
      setSavedSearchError("Unable to delete the saved search.");
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

    openCreateApplicationModal();
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
        <button
          type="button"
          onClick={() => {
            setShowSaveSearchForm(true);
            setSavedSearchError(null);
          }}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500">
          Save Search
        </button>

        {hasActiveFilters && (
          <button
            type="button"
            onClick={() => {
              setSearchTerm("");
              setApplicationFilter("ALL");
              setSourceFilter("ALL");
              setSortBy(
                discoveryPreferences?.discovery_default_sort ??
                  "BEST_MATCH_FIRST",
              );
              setLocationFilter("ALL");
            }}
            className="rounded-md border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800">
            Reset
          </button>
        )}
      </div>
      {showSaveSearchForm && (
        <div className="mb-6 rounded-lg border border-blue-500/40 bg-slate-900 p-4">
          <div className="mb-4 flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold text-white">
                Save Current Search
              </h2>

              <p className="text-sm text-slate-400">
                Save the current filters and sort order for later use.
              </p>
            </div>

            <button
              type="button"
              onClick={() => {
                setShowSaveSearchForm(false);
                setSavedSearchName("");
                setSavedSearchError(null);
              }}
              className="text-sm text-slate-400 hover:text-white">
              Cancel
            </button>
          </div>

          <div className="mb-4">
            <label className="mb-2 block text-sm text-slate-300">
              Search Name
            </label>

            <input
              type="text"
              value={savedSearchName}
              onChange={(event) => {
                setSavedSearchName(event.target.value);

                if (savedSearchError) {
                  setSavedSearchError(null);
                }
              }}
              placeholder="Technical Partnerships France"
              className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-blue-500"
            />
          </div>

          <div className="mb-4 grid gap-3 text-sm md:grid-cols-5">
            <div>
              <p className="text-slate-500">Keyword</p>
              <p className="text-slate-200">{searchTerm.trim() || "None"}</p>
            </div>

            <div>
              <p className="text-slate-500">Application Status</p>
              <p className="text-slate-200">{applicationFilter}</p>
            </div>

            <div>
              <p className="text-slate-500">Source</p>
              <p className="text-slate-200">{sourceFilter}</p>
            </div>

            <div>
              <p className="text-slate-500">Location</p>
              <p className="text-slate-200">{locationFilter}</p>
            </div>

            <div>
              <p className="text-slate-500">Sort</p>
              <p className="text-slate-200">{sortBy}</p>
            </div>
          </div>

          {savedSearchError && (
            <p className="mb-4 text-sm text-red-400">{savedSearchError}</p>
          )}

          <button
            type="button"
            onClick={handleSaveSearch}
            disabled={savingSearch}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60">
            {savingSearch ? "Saving..." : "Save Search"}
          </button>
        </div>
      )}

      <div className="mb-4 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <div>
          <p className="text-sm font-medium text-white">Opportunity Context</p>

          <p className="text-xs text-slate-400">
            Primary profile controls ranking, matching score display and
            application creation.
          </p>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="rounded bg-blue-600 px-2 py-1 text-xs text-white">
            Primary :
            {profiles.find((p) => p.id === selectedProfileId)?.profile_name}
          </span>

          <span className="rounded bg-green-600 px-2 py-1 text-xs text-white">
            Active:
            {activeProfileIds.length}
          </span>

          {bestProfileScore && (
            <span className="rounded bg-amber-500 px-2 py-1 text-xs text-black font-medium">
              Best:
              {bestProfileScore.profile_name}
            </span>
          )}
        </div>
        <div className="mt-4">
          <label className="mb-2 block text-sm text-slate-300">
            Primary Profile
          </label>

          <select
            value={selectedProfileId ?? ""}
            onChange={(event) => {
              const profileId = Number(event.target.value);

              setSelectedProfileId(profileId);

              setActiveProfileIds((current) =>
                current.includes(profileId) ? current : [...current, profileId],
              );
            }}
            className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white">
            {profiles.map((profile) => (
              <option key={profile.id} value={profile.id}>
                {profile.profile_name}
              </option>
            ))}
          </select>
        </div>

        <div className="mt-4">
          <p className="mb-2 text-sm text-slate-300">Active Profiles</p>

          <div className="space-y-2">
            {profiles.map((profile) => {
              const isPrimary = profile.id === selectedProfileId;

              return (
                <label
                  key={profile.id}
                  className="flex items-center gap-3 text-sm text-slate-300">
                  <input
                    type="checkbox"
                    checked={isActiveProfile(profile.id)}
                    disabled={isPrimary}
                    onChange={() => toggleActiveProfile(profile.id)}
                  />

                  <span>{profile.profile_name}</span>

                  {isPrimary && (
                    <span className="rounded bg-blue-600 px-2 py-0.5 text-xs text-white">
                      Primary
                    </span>
                  )}
                </label>
              );
            })}
          </div>
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

      <div className="mb-6 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">Saved Searches</h2>

            <p className="text-sm text-slate-400">
              Reapply frequently used opportunity filters.
            </p>
          </div>

          <span className="text-xs text-slate-500">
            {savedSearches.length} saved
          </span>
        </div>

        {savedSearches.length === 0 ? (
          <p className="text-sm text-slate-400">
            No saved searches yet. Save your first search configuration.
          </p>
        ) : (
          <div className="space-y-2">
            {savedSearches.map((savedSearch) => (
              <div
                key={savedSearch.id}
                className="flex flex-wrap items-center justify-between gap-3 rounded-md border border-slate-700 bg-slate-950 p-3">
                <div>
                  <p className="font-medium text-white">{savedSearch.name}</p>

                  <p className="text-xs text-slate-500">
                    Keyword: {savedSearch.keyword || "None"} · Status:{" "}
                    {savedSearch.application_status} · Source:{" "}
                    {savedSearch.source} · Location: {savedSearch.location} ·
                    Sort: {savedSearch.sort_by}
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => handleApplySavedSearch(savedSearch)}
                    className="rounded-md border border-blue-500 px-3 py-1.5 text-sm text-blue-300 hover:bg-blue-500/10">
                    Apply
                  </button>

                  <button
                    type="button"
                    onClick={() => handleDeleteSavedSearch(savedSearch.id)}
                    className="rounded-md border border-red-500/60 px-3 py-1.5 text-sm text-red-300 hover:bg-red-500/10">
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {savedSearchError && !showSaveSearchForm && (
          <p className="mt-3 text-sm text-red-400">{savedSearchError}</p>
        )}
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
      {isCreateApplicationModalOpen && selectedOffer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-xl rounded-lg border border-slate-700 bg-slate-900 p-6 shadow-xl">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-white">
                Create Application
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Review the profile assigned to this application before creating
                it.
              </p>
            </div>

            <div className="space-y-5">
              <div>
                <p className="text-sm font-medium text-slate-300">
                  Opportunity
                </p>

                <p className="mt-1 font-semibold text-white">
                  {selectedOffer.title}
                </p>

                <p className="text-sm text-slate-400">
                  {selectedOffer.company_name ?? "Unknown company"}
                </p>
              </div>

              <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-4">
                <p className="text-xs font-medium uppercase tracking-wide text-amber-300">
                  Best Matching Profile
                </p>

                {bestProfileScore ? (
                  <>
                    <p className="mt-1 font-semibold text-white">
                      {bestProfileScore.profile_name}
                    </p>

                    <p className="text-sm text-amber-200">
                      {Math.round(bestProfileScore.matching_score)}% match
                    </p>
                  </>
                ) : (
                  <p className="mt-1 text-sm text-slate-300">
                    Matching scores are unavailable. The Primary Profile has
                    been selected by default.
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="application-profile"
                  className="mb-2 block text-sm font-medium text-slate-300">
                  Application Profile
                </label>

                <select
                  id="application-profile"
                  value={applicationProfileId ?? ""}
                  disabled={creatingApplication}
                  onChange={(event) => {
                    setApplicationProfileId(Number(event.target.value));
                    setApplicationCreationError(null);
                  }}
                  className="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none focus:border-blue-500">
                  <option value="" disabled>
                    Select a profile
                  </option>

                  {profiles.map((profile) => (
                    <option key={profile.id} value={profile.id}>
                      {profile.profile_name}
                    </option>
                  ))}
                </select>

                <p className="mt-2 text-xs text-slate-400">
                  The selected profile will be permanently linked to the
                  application until explicitly changed.
                </p>
              </div>

              <div className="grid gap-3 text-sm sm:grid-cols-2">
                <div>
                  <p className="text-slate-500">Initial Status</p>
                  <p className="text-slate-200">Applied</p>
                </div>

                <div>
                  <p className="text-slate-500">Source</p>
                  <p className="text-slate-200">Opportunity</p>
                </div>
              </div>

              {applicationCreationError && (
                <p className="rounded-md border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">
                  {applicationCreationError}
                </p>
              )}
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                type="button"
                disabled={creatingApplication}
                onClick={closeCreateApplicationModal}
                className="rounded-md border border-slate-600 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50">
                Cancel
              </button>

              <button
                type="button"
                disabled={creatingApplication || applicationProfileId === null}
                onClick={handleCreateApplication}
                className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50">
                {creatingApplication ? "Creating..." : "Create Application"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
