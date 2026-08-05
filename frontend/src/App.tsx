import { useEffect, useState } from "react";

import { Dashboard } from "./components/Dashboard";
import { getProfiles, getJobOffers } from "./services/api";

function App() {
  const [profiles, setProfiles] = useState([]);
  const [jobOffers, setJobOffers] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const profilesData = await getProfiles();

        setProfiles(profilesData);

        const jobOffersData = await getJobOffers();

        setJobOffers(jobOffersData);
      } catch (error) {
        console.error("Erreur API :", error);

        setError("Unable to load data.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      {loading && <p>Loading...</p>}

      {error && <p>{error}</p>}

      {!loading && !error && (
        <Dashboard profiles={profiles} jobOffers={jobOffers} />
      )}
    </div>
  );
}

export default App;
