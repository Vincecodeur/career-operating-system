const API_BASE_URL = "http://127.0.0.1:8000";

export async function getProfiles() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/profiles`
        );

        console.log("HTTP Status:", response.status);

        const data = await response.json();

        console.log("Data reçue :", data);

        return data;
    } catch (error) {
        console.error("Erreur fetch :", error);
        throw error;
    }
}

export async function getJobOffers() {
    const response = await fetch(
        `${API_BASE_URL}/job-offers`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load job offers."
        );
    }

    return response.json();
}