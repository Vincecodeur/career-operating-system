import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { ApplicationSourceBadge } from "../components/ApplicationSourceBadge";
import { ApplicationStatusWorkflow } from "../components/ApplicationStatusWorkflow";
import { ApplicationTimeline } from "../components/ApplicationTimeline";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { StatCard } from "../components/ui/StatCard";
import {
  changeApplicationStatus,
  getApplications,
  getApplicationTimeline,
  getJobOffers,
  getMatching,
  getProfiles,
  updateApplication,
  type Application,
  type ApplicationEvent,
} from "../services/api";

type JobOfferSummary = {
  id: number;
  title: string;
  company_name: string | null;
};

type ProfileSummary = {
  id: number;
  full_name: string;
};

type MatchingSummary = {
  matching_score: number;
};

function getStatusColor(status: string) {
  switch (status) {
    case "Applied":
      return "text-yellow-400";

    case "Phone Screen":
      return "text-blue-400";

    case "Interview":
      return "text-cyan-400";

    case "Offer":
      return "text-purple-400";

    case "Accepted":
      return "text-green-400";

    case "Rejected":
      return "text-red-400";

    case "Withdrawn":
      return "text-slate-400";

    default:
      return "text-slate-300";
  }
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

export function ApplicationsPage() {
  const location = useLocation();

  const selectedApplicationId = (
    location.state as {
      applicationId?: number;
    } | null
  )?.applicationId;

  const navigate = useNavigate();

  const [applications, setApplications] = useState<Application[]>([]);
  const [selectedApplication, setSelectedApplication] =
    useState<Application | null>(null);

  const [timeline, setTimeline] = useState<ApplicationEvent[]>([]);
  const [notesDraft, setNotesDraft] = useState("");
  const [sourceDraft, setSourceDraft] = useState("MANUAL");

  const [jobOfferTitles, setJobOfferTitles] = useState<Record<number, string>>(
    {},
  );
  const [jobOfferCompanies, setJobOfferCompanies] = useState<
    Record<number, string>
  >({});
  const [profileNames, setProfileNames] = useState<Record<number, string>>({});
  const [matchingScore, setMatchingScore] = useState<number | null>(null);

  const [loading, setLoading] = useState(true);
  const [savingNotes, setSavingNotes] = useState(false);
  const [savingSource, setSavingSource] = useState(false);
  const [changingStatus, setChangingStatus] = useState(false);
  const [matchingLoading, setMatchingLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const [actionMessage, setActionMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  function getJobOfferTitle(jobOfferId: number) {
    return jobOfferTitles[jobOfferId] ?? `Job Offer ${jobOfferId}`;
  }

  function getJobOfferCompany(jobOfferId: number) {
    return jobOfferCompanies[jobOfferId] ?? "Unknown company";
  }

  function getProfileName(profileId: number) {
    const profileName = profileNames[profileId];

    if (
      !profileName ||
      profileName.trim() === "" ||
      profileName.trim().toLowerCase() === "string"
    ) {
      return `Profile ${profileId}`;
    }

    return profileName;
  }

  async function loadTimeline(applicationId: number) {
    try {
      const events = await getApplicationTimeline(applicationId);
      setTimeline(events);
    } catch {
      setTimeline([]);
    }
  }

  async function loadMatchingScore(application: Application) {
    setMatchingLoading(true);

    try {
      const matching = (await getMatching(
        application.profile_id,
        application.job_offer_id,
      )) as MatchingSummary;

      setMatchingScore(matching.matching_score);
    } catch {
      setMatchingScore(null);
    } finally {
      setMatchingLoading(false);
    }
  }

  function replaceApplicationInList(updatedApplication: Application) {
    setApplications((currentApplications) =>
      currentApplications.map((application) =>
        application.id === updatedApplication.id
          ? updatedApplication
          : application,
      ),
    );
  }

  async function selectApplication(application: Application) {
    setSelectedApplication(application);
    setNotesDraft(application.notes ?? "");
    setSourceDraft(application.source_type);
    setActionMessage(null);

    await Promise.all([
      loadTimeline(application.id),
      loadMatchingScore(application),
    ]);
  }

  useEffect(() => {
    async function loadApplications() {
      try {
        const [applicationsData, offersData, profilesData] = await Promise.all([
          getApplications(),
          getJobOffers(),
          getProfiles(),
        ]);

        const applicationList = Array.isArray(applicationsData)
          ? applicationsData
          : (applicationsData.value ?? []);

        const offers = Array.isArray(offersData)
          ? (offersData as JobOfferSummary[])
          : [];

        const profiles = Array.isArray(profilesData)
          ? (profilesData as ProfileSummary[])
          : [];

        setJobOfferTitles(
          Object.fromEntries(offers.map((offer) => [offer.id, offer.title])),
        );

        setJobOfferCompanies(
          Object.fromEntries(
            offers.map((offer) => [
              offer.id,
              offer.company_name ?? "Unknown company",
            ]),
          ),
        );

        setProfileNames(
          Object.fromEntries(
            profiles.map((profile) => [profile.id, profile.full_name]),
          ),
        );

        const sortedApplications = [...applicationList].sort(
          (firstApplication, secondApplication) =>
            new Date(secondApplication.created_at).getTime() -
            new Date(firstApplication.created_at).getTime(),
        );

        setApplications(sortedApplications);

        if (sortedApplications.length > 0) {
          const preselectedApplication =
            selectedApplicationId !== undefined
              ? sortedApplications.find(
                  (application) => application.id === selectedApplicationId,
                )
              : null;

          const applicationToSelect =
            preselectedApplication ?? sortedApplications[0];

          setSelectedApplication(applicationToSelect);

          setNotesDraft(applicationToSelect.notes ?? "");

          setSourceDraft(applicationToSelect.source_type);

          await Promise.all([
            loadTimeline(applicationToSelect.id),
            loadMatchingScore(applicationToSelect),
          ]);
        }
      } catch {
        setError("Unable to load applications.");
      } finally {
        setLoading(false);
      }
    }

    loadApplications();
  }, [selectedApplicationId]);

  const applicationStats = useMemo(() => {
    const appliedCount = applications.filter(
      (application) => application.status === "Applied",
    ).length;

    const interviewCount = applications.filter(
      (application) => application.status === "Interview",
    ).length;

    const offerCount = applications.filter(
      (application) => application.status === "Offer",
    ).length;

    const acceptedCount = applications.filter(
      (application) => application.status === "Accepted",
    ).length;

    return {
      total: applications.length,
      applied: appliedCount,
      interview: interviewCount,
      offers: offerCount,
      accepted: acceptedCount,
    };
  }, [applications]);

  async function handleSaveNotes() {
    if (!selectedApplication) {
      return;
    }

    setSavingNotes(true);
    setActionMessage(null);

    try {
      const updatedApplication = await updateApplication(
        selectedApplication.id,
        {
          status: selectedApplication.status,
          notes: notesDraft,
          source_type: selectedApplication.source_type,
        },
      );

      setSelectedApplication(updatedApplication);
      replaceApplicationInList(updatedApplication);
      setSourceDraft(updatedApplication.source_type);

      setActionMessage({
        type: "success",
        text: "Notes saved successfully.",
      });
    } catch (error) {
      setActionMessage({
        type: "error",
        text: error instanceof Error ? error.message : "Unable to save notes.",
      });
    } finally {
      setSavingNotes(false);
    }
  }

  async function handleSaveSource() {
    if (!selectedApplication) {
      return;
    }

    setSavingSource(true);
    setActionMessage(null);

    try {
      const updatedApplication = await updateApplication(
        selectedApplication.id,
        {
          status: selectedApplication.status,
          notes: notesDraft,
          source_type: sourceDraft,
        },
      );

      setSelectedApplication(updatedApplication);
      replaceApplicationInList(updatedApplication);
      setNotesDraft(updatedApplication.notes ?? "");
      setSourceDraft(updatedApplication.source_type);

      setActionMessage({
        type: "success",
        text: "Source updated successfully.",
      });
    } catch (error) {
      setActionMessage({
        type: "error",
        text:
          error instanceof Error ? error.message : "Unable to update source.",
      });
    } finally {
      setSavingSource(false);
    }
  }

  async function handleStatusChange(status: string) {
    if (!selectedApplication) {
      return;
    }

    setChangingStatus(true);
    setActionMessage(null);

    try {
      const updatedApplication = await changeApplicationStatus(
        selectedApplication.id,
        {
          status,
        },
      );

      setSelectedApplication(updatedApplication);
      replaceApplicationInList(updatedApplication);
      setNotesDraft(updatedApplication.notes ?? "");
      setSourceDraft(updatedApplication.source_type);

      await Promise.all([
        loadTimeline(updatedApplication.id),
        loadMatchingScore(updatedApplication),
      ]);

      setActionMessage({
        type: "success",
        text: `Application moved to ${updatedApplication.status}.`,
      });
    } catch (error) {
      setActionMessage({
        type: "error",
        text:
          error instanceof Error ? error.message : "Unable to update status.",
      });
    } finally {
      setChangingStatus(false);
    }
  }

  return (
    <>
      <PageHeader title="Applications" description="Track job applications." />

      {loading && <p className="text-slate-400">Loading applications...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <>
          <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-5">
            <StatCard
              title="Total Applications"
              value={applicationStats.total}
            />

            <StatCard title="Applied" value={applicationStats.applied} />

            <StatCard title="Interview" value={applicationStats.interview} />

            <StatCard title="Offers" value={applicationStats.offers} />

            <StatCard title="Accepted" value={applicationStats.accepted} />
          </div>

          {applications.length === 0 ? (
            <Card>
              <p className="text-slate-400">No applications available.</p>
            </Card>
          ) : (
            <div className="grid gap-6 lg:grid-cols-3">
              <div className="max-h-[calc(100vh-260px)] space-y-3 overflow-y-auto pr-2">
                {applications.map((application) => (
                  <button
                    key={application.id}
                    type="button"
                    onClick={() => selectApplication(application)}
                    className={`block w-full rounded-lg text-left transition-all ${
                      selectedApplication?.id === application.id
                        ? "border-2 border-blue-500 bg-slate-800 shadow-lg shadow-blue-500/20"
                        : ""
                    }`}>
                    <Card>
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="text-xs uppercase text-slate-400">
                            Application
                          </p>

                          <h3 className="mt-1 text-lg font-semibold text-white">
                            {getJobOfferTitle(application.job_offer_id)}
                          </h3>

                          <p className="mt-1 text-sm text-slate-400">
                            {getJobOfferCompany(application.job_offer_id)}
                          </p>

                          <div className="mt-3">
                            <ApplicationSourceBadge
                              sourceType={application.source_type}
                            />
                          </div>
                        </div>

                        <span
                          className={`text-sm font-semibold ${getStatusColor(
                            application.status,
                          )}`}>
                          {application.status}
                        </span>
                      </div>
                    </Card>
                  </button>
                ))}
              </div>

              <div className="sticky top-6 self-start lg:col-span-2">
                {selectedApplication ? (
                  <Card>
                    <div className="mb-8">
                      <p className="text-sm uppercase text-slate-400">
                        Application Detail
                      </p>

                      <h2 className="mt-2 text-3xl font-bold text-white">
                        {getJobOfferTitle(selectedApplication.job_offer_id)}
                      </h2>

                      <p className="mt-1 text-slate-400">
                        {getJobOfferCompany(selectedApplication.job_offer_id)}
                      </p>

                      <p
                        className={`mt-2 font-semibold ${getStatusColor(
                          selectedApplication.status,
                        )}`}>
                        {selectedApplication.status}
                      </p>

                      {matchingLoading && (
                        <p className="mt-3 text-sm text-slate-400">
                          Loading match score...
                        </p>
                      )}

                      {!matchingLoading && matchingScore !== null && (
                        <div className="mt-3 rounded-md bg-blue-500/10 px-3 py-2">
                          <p className="text-sm font-medium text-blue-300">
                            Match Score: {matchingScore}%
                          </p>
                        </div>
                      )}

                      {actionMessage && (
                        <div
                          className={`mt-3 rounded-md border px-3 py-2 text-sm ${
                            actionMessage.type === "success"
                              ? "border-green-500/40 bg-green-500/10 text-green-300"
                              : "border-red-500/40 bg-red-500/10 text-red-300"
                          }`}>
                          {actionMessage.text}
                        </div>
                      )}
                    </div>

                    <div className="mb-8 grid grid-cols-2 gap-4 text-sm text-slate-400">
                      <div>
                        <p className="font-medium text-slate-300">Profile</p>

                        <p>{getProfileName(selectedApplication.profile_id)}</p>

                        <button
                          type="button"
                          onClick={() =>
                            navigate("/profiles", {
                              state: {
                                profileId: selectedApplication.profile_id,
                              },
                            })
                          }
                          className="mt-2 rounded-md border border-blue-500 px-3 py-1 text-sm text-blue-300 hover:bg-blue-500/10">
                          Open Profile
                        </button>
                      </div>

                      <div>
                        <p className="font-medium text-slate-300">
                          Opportunity
                        </p>

                        <p>
                          {getJobOfferTitle(selectedApplication.job_offer_id)}
                        </p>

                        <button
                          type="button"
                          onClick={() =>
                            navigate("/opportunities", {
                              state: {
                                jobOfferId: selectedApplication.job_offer_id,
                              },
                            })
                          }
                          className="mt-2 rounded-md border border-blue-500 px-3 py-1 text-sm text-blue-300 hover:bg-blue-500/10">
                          Open Opportunity
                        </button>
                      </div>

                      <div>
                        <p className="font-medium text-slate-300">Created At</p>

                        <p>{formatDate(selectedApplication.created_at)}</p>
                      </div>

                      <div>
                        <p className="font-medium text-slate-300">Updated At</p>

                        <p>{formatDate(selectedApplication.updated_at)}</p>
                      </div>
                    </div>

                    <div className="space-y-8">
                      <div>
                        <h3 className="mb-3 text-lg font-semibold text-white">
                          Source
                        </h3>

                        <div className="mb-3">
                          <ApplicationSourceBadge
                            sourceType={selectedApplication.source_type}
                          />
                        </div>

                        <div className="flex flex-wrap items-center gap-3">
                          <select
                            value={sourceDraft}
                            onChange={(event) =>
                              setSourceDraft(event.target.value)
                            }
                            className="rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none focus:border-blue-500">
                            <option value="MANUAL">MANUAL</option>
                            <option value="REFERRAL">REFERRAL</option>
                            <option value="OPPORTUNITY">OPPORTUNITY</option>
                            <option value="EXTERNAL">EXTERNAL</option>
                          </select>

                          <button
                            type="button"
                            disabled={
                              savingSource ||
                              sourceDraft === selectedApplication.source_type
                            }
                            onClick={handleSaveSource}
                            className="rounded-md border border-blue-500 px-4 py-2 text-sm font-medium text-blue-300 transition hover:bg-blue-500/10 disabled:cursor-not-allowed disabled:opacity-50">
                            {savingSource ? "Saving..." : "Save Source"}
                          </button>
                        </div>
                      </div>

                      <div>
                        <h3 className="mb-3 text-lg font-semibold text-white">
                          Workflow
                        </h3>

                        <ApplicationStatusWorkflow
                          currentStatus={selectedApplication.status}
                          disabled={changingStatus}
                          onStatusChange={handleStatusChange}
                        />
                      </div>

                      <div>
                        <h3 className="mb-3 text-lg font-semibold text-white">
                          Notes
                        </h3>

                        <textarea
                          value={notesDraft}
                          onChange={(event) =>
                            setNotesDraft(event.target.value)
                          }
                          rows={6}
                          className="w-full rounded-md border border-slate-700 bg-slate-950 p-3 text-sm text-white outline-none focus:border-blue-500"
                          placeholder="Add recruiter feedback, interview notes, salary details or follow-up actions."
                        />

                        <button
                          type="button"
                          disabled={savingNotes}
                          onClick={handleSaveNotes}
                          className="mt-3 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50">
                          {savingNotes ? "Saving..." : "Save Notes"}
                        </button>
                      </div>

                      <div>
                        <h3 className="mb-3 text-lg font-semibold text-white">
                          Timeline
                        </h3>

                        <ApplicationTimeline events={timeline} />
                      </div>
                    </div>
                  </Card>
                ) : (
                  <Card>
                    <p className="text-slate-400">
                      Select an application to view details.
                    </p>
                  </Card>
                )}
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}
