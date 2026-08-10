import { useEffect, useMemo, useState } from "react";

import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { StatCard } from "../components/ui/StatCard";
import { getApplications } from "../services/api";

type Application = {
  id: number;
  profile_id: number;
  job_offer_id: number;
  status: string;
  created_at: string;
  updated_at: string;
};

function getStatusColor(status: string) {
  switch (status) {
    case "Applied":
      return "text-yellow-400";

    case "Interview":
      return "text-cyan-400";

    case "Not Applied":
      return "text-slate-400";

    case "Accepted":
      return "text-green-400";

    case "Rejected":
      return "text-red-400";

    default:
      return "text-slate-300";
  }
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

export function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [selectedApplication, setSelectedApplication] =
    useState<Application | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadApplications() {
      try {
        const data = await getApplications();

        const applicationList = Array.isArray(data) ? data : (data.value ?? []);

        const sortedApplications = [...applicationList].sort(
          (firstApplication, secondApplication) =>
            new Date(secondApplication.created_at).getTime() -
            new Date(firstApplication.created_at).getTime(),
        );

        setApplications(sortedApplications);

        if (sortedApplications.length > 0) {
          setSelectedApplication(sortedApplications[0]);
        }
      } catch {
        setError("Unable to load applications.");
      } finally {
        setLoading(false);
      }
    }

    loadApplications();
  }, []);

  const applicationStats = useMemo(() => {
    const appliedCount = applications.filter(
      (application) => application.status === "Applied",
    ).length;

    const interviewCount = applications.filter(
      (application) => application.status === "Interview",
    ).length;

    const notAppliedCount = applications.filter(
      (application) => application.status === "Not Applied",
    ).length;

    return {
      total: applications.length,
      applied: appliedCount,
      interview: interviewCount,
      notApplied: notAppliedCount,
    };
  }, [applications]);

  return (
    <>
      <PageHeader title="Applications" description="Track job applications." />

      {loading && <p className="text-slate-400">Loading applications...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <>
          <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-4">
            <StatCard
              title="Total Applications"
              value={applicationStats.total}
            />

            <StatCard title="Applied" value={applicationStats.applied} />

            <StatCard title="Interview" value={applicationStats.interview} />

            <StatCard title="Not Applied" value={applicationStats.notApplied} />
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
                    onClick={() => setSelectedApplication(application)}
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
                            #{application.id}
                          </h3>

                          <p className="mt-1 text-sm text-slate-400">
                            Job Offer {application.job_offer_id}
                          </p>
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
                        Application #{selectedApplication.id}
                      </h2>

                      <p
                        className={`mt-2 font-semibold ${getStatusColor(
                          selectedApplication.status,
                        )}`}>
                        {selectedApplication.status}
                      </p>
                    </div>

                    <div className="mb-8 grid grid-cols-2 gap-4 text-sm text-slate-400">
                      <div>
                        <p className="font-medium text-slate-300">Profile ID</p>

                        <p>{selectedApplication.profile_id}</p>
                      </div>

                      <div>
                        <p className="font-medium text-slate-300">
                          Job Offer ID
                        </p>

                        <p>{selectedApplication.job_offer_id}</p>
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

                    <div className="border-t border-slate-700 pt-6">
                      <h3 className="mb-3 text-lg font-semibold text-white">
                        Application Workflow
                      </h3>

                      <p className="text-slate-400">
                        Application workflow management will be added in Phase
                        7.1.17.
                      </p>
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
