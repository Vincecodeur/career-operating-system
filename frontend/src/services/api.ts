const API_BASE_URL = "http://127.0.0.1:8000";

export async function getProfiles() {
    const response = await fetch(
        `${API_BASE_URL}/profiles`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profiles."
        );
    }

    return response.json();
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

export async function getMatching(
    profileId: number,
    jobOfferId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/matching/${profileId}/${jobOfferId}`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load matching result."
        );
    }

    return response.json();
}