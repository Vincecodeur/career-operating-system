import { useEffect, useState } from "react";

import { getProfiles } from "./services/api";

function App() {
  const [profiles, setProfiles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfiles() {
      try {
        const data = await getProfiles();

        setProfiles(data);
      } catch (error) {
        console.error("Erreur API :", error);

        setError("Unable to load profiles.");
      } finally {
        setLoading(false);
      }
    }

    loadProfiles();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Career Operating System</h1>

      {loading && <p>Loading...</p>}

      {error && <p>{error}</p>}

      <h2>Profiles</h2>

      <ul>
        {profiles.map((profile) => (
          <li key={profile.id}>{profile.full_name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
