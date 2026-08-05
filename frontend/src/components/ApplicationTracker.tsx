type Application = {
  id: number;
  profile_id: number;
  job_offer_id: number;
  status: string;
};

type Props = {
  applications: Application[];
};

export function ApplicationTracker({ applications }: Props) {
  return (
    <section>
      <h2>Applications</h2>

      <ul>
        {applications.map((application) => (
          <li key={application.id}>
            Application #{application.id}
            <br />
            Profile : {application.profile_id}
            <br />
            Job Offer : {application.job_offer_id}
            <br />
            Status : {application.status}
          </li>
        ))}
      </ul>
    </section>
  );
}
