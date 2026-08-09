import { useEffect, useState } from "react";

import { Dashboard } from "./components/Dashboard";
import {
  getApplications,
  getJobOffers,
  getMatching,
  getProfiles,
  getRankedJobOffers,
} from "./services/api";

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

  skills_score: number;
  experience_score: number;
  work_mode_score: number;
  location_score: number;

  matching_skills: string[];
  missing_skills: string[];

  strengths: string[];
  weaknesses: string[];
  explanations: {
    criterion: string;
    score: number;
    message: string;
  }[];
};

type RankedJobOffer = {
  job_offer_id: number;
  title: string;

  matching_score: number;

  skills_score: number;
  experience_score: number;
  work_mode_score: number;
  location_score: number;

  matching_skills: string[];
  missing_skills: string[];
};

type Application = {
  id: number;
  profile_id: number;
  job_offer_id: number;
  status: string;
};

function App() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [jobOffers, setJobOffers] = useState<JobOffer[]>([]);
  const [matching, setMatching] = useState<Matching | null>(null);
  const [rankedJobOffers, setRankedJobOffers] = useState<RankedJobOffer[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const profilesData = await getProfiles();
        const jobOffersData = await getJobOffers();
        const applicationsData = await getApplications();

        setProfiles(profilesData);
        setJobOffers(jobOffersData);
        setApplications(applicationsData);

        if (profilesData.length > 0 && jobOffersData.length > 0) {
          const matchingData = await getMatching(
            profilesData[0].id,
            jobOffersData[0].id,
          );
          const rankedData = await getRankedJobOffers(profilesData[0].id);

          setRankedJobOffers(rankedData);
          setMatching(matchingData);
        }
      } catch (error) {
        console.error("Erreur API :", error);

        setError("Unable to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboardData();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      {loading && <p>Loading...</p>}

      {error && <p>{error}</p>}

      {!loading && !error && (
        <Dashboard
          profiles={profiles}
          jobOffers={jobOffers}
          matching={matching}
          rankedJobOffers={rankedJobOffers}
          applications={applications}
        />
      )}
    </div>
  );
}

export default App;
