type Application = {
  id: number;
  profile_id: number;
  job_offer_id: number;
  status: string;
};

type Props = {
  applications: Application[];
};

function getStatusColor(status: string) {
  switch (status) {
    case "Accepted":
      return "text-green-400";

    case "Interview":
      return "text-cyan-400";

    case "Applied":
      return "text-yellow-400";

    case "Rejected":
      return "text-red-400";

    default:
      return "text-slate-300";
  }
}

export function ApplicationTracker({ applications }: Props) {
  return (
    <div className="space-y-3">
      {applications.map((application) => (
        <div
          key={application.id}
          className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-white">
                Application #{application.id}
              </h3>

              <p className="text-sm text-slate-400">
                Profile {application.profile_id}
              </p>

              <p className="text-sm text-slate-400">
                Job Offer {application.job_offer_id}
              </p>
            </div>

            <span
              className={`font-semibold ${getStatusColor(application.status)}`}>
              {application.status}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
