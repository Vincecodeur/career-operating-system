import { JobOfferList } from "./JobOfferList";
import { MatchingResult } from "./MatchingResult";
import { ProfileList } from "./ProfileList";

type Profile = {
  id: number;
  full_name: string;
};

type JobOffer = {
  id: number;
  title: string;
};

type Matching = {
  profile_id: number;
  job_offer_id: number;
  matching_score: number;
  matching_skills: string[];
  missing_skills: string[];
};

type Props = {
  profiles: Profile[];
  jobOffers: JobOffer[];
  matching: Matching | null;
};

export function Dashboard({ profiles, jobOffers, matching }: Props) {
  return (
    <>
      <h1>Career Operating System</h1>

      <ProfileList profiles={profiles} />

      <JobOfferList jobOffers={jobOffers} />

      {matching && (
        <MatchingResult
          matchingScore={matching.matching_score}
          matchingSkills={matching.matching_skills}
          missingSkills={matching.missing_skills}
        />
      )}
    </>
  );
}
