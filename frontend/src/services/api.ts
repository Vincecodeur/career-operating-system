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

export async function getProfile(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile."
        );
    }

    return response.json();
}

type ProfilePayload = {
    profile_name: string;
    full_name: string;
    current_title: string;
    location: string;
    years_of_experience: number;
    target_role_short_term: string;
    target_role_long_term: string;
    remote_preference: string;
    preferred_countries: string;
};

export async function updateProfile(
    profileId: number,
    payload: ProfilePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update profile."
        );
    }

    return response.json();
}

export async function deleteProfile(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to archive profile."
        );
    }

    return response.json();
}

export async function getProfileSkills(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/skills`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile skills."
        );
    }

    return response.json();
}

export async function getSkills() {
    const response = await fetch(
        `${API_BASE_URL}/skills`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load skills."
        );
    }

    return response.json();
}

export async function getProfileWorkExperiences(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/work-experiences`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile work experiences."
        );
    }

    return response.json();
}

export async function getLanguages() {
    const response = await fetch(
        `${API_BASE_URL}/languages`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load languages."
        );
    }

    return response.json();
}

export async function getProfileLanguages(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/languages`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile languages."
        );
    }

    return response.json();
}

export async function getCertifications() {
    const response = await fetch(
        `${API_BASE_URL}/certifications`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load certifications."
        );
    }

    return response.json();
}

export async function getProfileCertifications(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/certifications`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile certifications."
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

export async function getRankedJobOffers(
    profileId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/ranked-job-offers`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load ranked job offers."
        );
    }

    return response.json();
}

export async function getApplications() {
    const response = await fetch(
        `${API_BASE_URL}/applications`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load applications."
        );
    }

    return response.json();
}