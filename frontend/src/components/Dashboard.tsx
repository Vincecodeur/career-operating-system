import { JobOfferList } from "./JobOfferList";
import { MatchingResult } from "./MatchingResult";
import { ProfileList } from "./ProfileList";
import { OpportunityRanking } from "./OpportunityRanking";
import { ApplicationTracker } from "./ApplicationTracker";

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

type RankedJobOffer = {
  job_offer_id: number;
  title: string;
  matching_score: number;
  matching_skills: string[];
  missing_skills: string[];
};

type Application = {
  id: number;
  profile_id: number;
  job_offer_id: number;
  status: string;
};

type Props = {
  profiles: Profile[];
  jobOffers: JobOffer[];
  matching: Matching | null;
  rankedJobOffers: RankedJobOffer[];
  applications: Application[];
};

export function Dashboard({
  profiles,
  jobOffers,
  matching,
  rankedJobOffers,
  applications,
}: Props) {
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
      <OpportunityRanking rankedJobOffers={rankedJobOffers} />
      <ApplicationTracker applications={applications} />
    </>
  );
}
