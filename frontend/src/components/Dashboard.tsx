import { ApplicationTracker } from "./ApplicationTracker";
import { JobOfferList } from "./JobOfferList";
import { MatchingResult } from "./MatchingResult";
import { OpportunityRanking } from "./OpportunityRanking";
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
      <section>
        <h1>Dashboard</h1>
        <p>Overview of profiles, opportunities and applications.</p>
      </section>
      <section>
        <h2>Overview</h2>

        <ul>
          <li>Profiles: {profiles.length}</li>

          <li>Job Offers: {jobOffers.length}</li>

          <li>Applications: {applications.length}</li>

          <li>Top Match: {matching ? `${matching.matching_score}%` : "N/A"}</li>
        </ul>
      </section>
      <section>
        <h2>Profiles</h2>
        <ProfileList profiles={profiles} />
      </section>

      <section>
        <h2>Opportunities</h2>

        <JobOfferList jobOffers={jobOffers} />

        <OpportunityRanking rankedJobOffers={rankedJobOffers} />
      </section>

      <section>
        <h2>Matching Analysis</h2>

        {matching && (
          <MatchingResult
            matchingScore={matching.matching_score}
            matchingSkills={matching.matching_skills}
            missingSkills={matching.missing_skills}
          />
        )}
      </section>

      <section>
        <h2>Applications</h2>

        <ApplicationTracker applications={applications} />
      </section>
    </>
  );
}
