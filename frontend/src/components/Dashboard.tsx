import { ProfileList } from "./ProfileList";
import { JobOfferList } from "./JobOfferList";

type Profile = {
  id: number;
  full_name: string;
};

type JobOffer = {
  id: number;
  title: string;
};

type Props = {
  profiles: Profile[];
  jobOffers: JobOffer[];
};

export function Dashboard({ profiles, jobOffers }: Props) {
  return (
    <>
      <h1>Career Operating System</h1>

      <ProfileList profiles={profiles} />
      <JobOfferList jobOffers={jobOffers} />
    </>
  );
}
