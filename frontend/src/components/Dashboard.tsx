import { ApplicationTracker } from "./ApplicationTracker";

import { MatchingResult } from "./MatchingResult";
import { OpportunityRanking } from "./OpportunityRanking";
import { ProfileList } from "./ProfileList";
import { PageHeader } from "./ui/PageHeader";
import { Section } from "./ui/Section";
import { StatCard } from "./ui/StatCard";

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
        <PageHeader
          title="Dashboard"
          description="Overview of profiles, opportunities and applications."
        />
      </section>
      <Section title="Overview">
        <div className="grid grid-cols-4 gap-4">
          <StatCard title="Profiles" value={profiles.length} />

          <StatCard title="Job Offers" value={jobOffers.length} />

          <StatCard title="Applications" value={applications.length} />

          <StatCard
            title="Top Match"
            value={matching ? `${matching.matching_score}%` : "N/A"}
          />
        </div>
      </Section>
      <Section title="Profiles">
        <h2>Profiles</h2>
        <ProfileList profiles={profiles} />
      </Section>

      <Section title="Opportunities">
        <h2>Opportunities</h2>

        <OpportunityRanking rankedJobOffers={rankedJobOffers} />
      </Section>

      <Section title="Matching Analysis">
        <h2>Matching Analysis</h2>

        {matching && (
          <MatchingResult
            matchingScore={matching.matching_score}
            matchingSkills={matching.matching_skills}
            missingSkills={matching.missing_skills}
          />
        )}
      </Section>

      <Section title="Applications">
        <h2>Applications</h2>

        <ApplicationTracker applications={applications} />
      </Section>
    </>
  );
}
