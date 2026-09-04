import { useAuthStore } from "../stores/authStore";

const API_BASE_URL = "http://127.0.0.1:8000";

function getAuthHeaders(): Record<string, string> {
    const token = useAuthStore.getState().accessToken;

    if (!token) {
        return {};
    }

    return {
        Authorization: `Bearer ${token}`,
    };
}

async function getApiErrorMessage(
    response: Response,
    fallbackMessage: string,
): Promise<string> {
    try {
        const data = await response.json();

        if (
            data &&
            typeof data.detail === "string"
        ) {
            return data.detail;
        }

        return fallbackMessage;
    } catch {
        return fallbackMessage;
    }
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

type ProfileSkillPayload = {
    profile_id: number;
    skill_id: number;
    years_of_experience: number;
    self_assessment_level: string;
};

type ProfileSkillUpdatePayload = {
    years_of_experience: number;
    self_assessment_level: string;
};

type ProfileSoftSkillPayload = {
    profile_id: number;
    name: string;
};

export type Skill = {
    id: number;
    name: string;
    category: string;
    created_at: string;
};
export type ProfileSoftSkill = {
    id: number;
    profile_id: number;
    name: string;
    created_at: string;
};

export type ReferenceDataItem = {
    id: number;
    code: string;
    name: string;
};

type ProfileLanguagePayload = {
    profile_id: number;
    language_id: number;
    proficiency_level: string;
};

type ProfileLanguageUpdatePayload = {
    proficiency_level: string;
};

type WorkExperiencePayload = {
    profile_id: number;
    company_name: string;
    job_title: string;
    start_date: string;
    end_date: string | null;
    is_current_position: boolean;
    description: string;
};

type WorkExperienceUpdatePayload = {
    company_name: string;
    job_title: string;
    start_date: string;
    end_date: string | null;
    is_current_position: boolean;
    description: string;
};

type ProfileCertificationPayload = {
    profile_id: number;
    certification_id: number;
    obtained_date: string | null;
    expiration_date: string | null;
    credential_id: string | null;
};

type ProfileCertificationUpdatePayload = {
    obtained_date: string | null;
    expiration_date: string | null;
    credential_id: string | null;
};

export type Cv = {
    id: number;
    profile_id: number;
    file_name: string;
    original_file_name: string;
    storage_path: string;
    file_size_bytes: number;
    mime_type: string;
    language: string | null;
    version_label: string | null;
    is_default: boolean;
    parsing_status: string;
    uploaded_at: string;
    updated_at: string;
};

type CvUpdatePayload = {
    language: string | null;
    version_label: string | null;
};

export type ProfileEnrichmentProposal = {
    id: number;
    profile_id: number;
    cv_id: number;
    proposal_type: string;
    status: string;
    source_field: string;
    target_field: string;
    observed_value: string;
    normalized_value: string;
    current_profile_value: string | null;
    proposed_value: string;
    reference_id: number | null;
    conflict_detected: boolean;
    rejection_reason: string | null;
    created_at: string;
    validated_at: string | null;
};

type AcceptProfileEnrichmentPayload = {
    proposed_value_override?: string | null;
    reference_id?: number | null;
};

export async function getWorkModes(): Promise<ReferenceDataItem[]> {
    const response = await fetch(
        `${API_BASE_URL}/reference-data/work-modes`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load work modes."
        );
    }

    return response.json();
}

export async function getCountries(): Promise<ReferenceDataItem[]> {
    const response = await fetch(
        `${API_BASE_URL}/reference-data/countries`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load countries."
        );
    }

    return response.json();
}

export async function getProfiles() {
    const response = await fetch(
        `${API_BASE_URL}/profiles`,
        {
            headers: getAuthHeaders(),
        },
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
        `${API_BASE_URL}/profiles/${profileId}`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile."
        );
    }

    return response.json();
}

export async function createProfile(
    payload: ProfilePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profiles`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to create profile."
        );
    }

    return response.json();
}

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
                ...getAuthHeaders(),
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
            headers: getAuthHeaders(),
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
        `${API_BASE_URL}/profiles/${profileId}/skills`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile skills."
        );
    }

    return response.json();
}

export async function createProfileSkill(
    payload: ProfileSkillPayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-skills`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to add profile skill."
        );
    }

    return response.json();
}

export async function updateProfileSkill(
    profileId: number,
    skillId: number,
    payload: ProfileSkillUpdatePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-skills/${profileId}/${skillId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update profile skill."
        );
    }

    return response.json();
}

export async function deleteProfileSkill(
    profileId: number,
    skillId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-skills/${profileId}/${skillId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders(),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to remove profile skill."
        );
    }

    return response.json();
}

export async function getProfileSoftSkills(
    profileId: number,
): Promise<ProfileSoftSkill[]> {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/soft-skills`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile soft skills."
        );
    }

    return response.json();
}

export async function createProfileSoftSkill(
    payload: ProfileSoftSkillPayload,
): Promise<ProfileSoftSkill> {
    const response = await fetch(
        `${API_BASE_URL}/profile-soft-skills`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to add profile soft skill."
        );
    }

    return response.json();
}

export async function deleteProfileSoftSkill(
    softSkillId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-soft-skills/${softSkillId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders(),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to remove profile soft skill."
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
        `${API_BASE_URL}/profiles/${profileId}/work-experiences`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile work experiences."
        );
    }

    return response.json();
}

export async function createWorkExperience(
    payload: WorkExperiencePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/work-experiences`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to add work experience.",
        );
    }

    return response.json();
}

export async function updateWorkExperience(
    workExperienceId: number,
    payload: WorkExperienceUpdatePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/work-experiences/${workExperienceId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update work experience.",
        );
    }

    return response.json();
}

export async function deleteWorkExperience(
    workExperienceId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/work-experiences/${workExperienceId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to remove work experience.",
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
        `${API_BASE_URL}/profiles/${profileId}/languages`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile languages."
        );
    }

    return response.json();
}

export async function createProfileLanguage(
    payload: ProfileLanguagePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-languages`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to add profile language."
        );
    }

    return response.json();
}

export async function updateProfileLanguage(
    profileId: number,
    languageId: number,
    payload: ProfileLanguageUpdatePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-languages/${profileId}/${languageId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update profile language."
        );
    }

    return response.json();
}

export async function deleteProfileLanguage(
    profileId: number,
    languageId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-languages/${profileId}/${languageId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders(),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to remove profile language."
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
        `${API_BASE_URL}/profiles/${profileId}/certifications`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile certifications."
        );
    }

    return response.json();
}

export async function getProfileCvs(
    profileId: number,
): Promise<Cv[]> {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/cvs`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load CVs."
        );
    }

    return response.json();
}

export async function uploadCv(
    profileId: number,
    file: File,
    language?: string,
    versionLabel?: string,
    isDefault = false,
): Promise<Cv> {
    const formData = new FormData();

    formData.append("cv_file", file);

    if (language) {
        formData.append("language", language);
    }

    if (versionLabel) {
        formData.append(
            "version_label",
            versionLabel,
        );
    }

    formData.append(
        "is_default",
        String(isDefault),
    );

    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/cvs`,
        {
            method: "POST",
            headers: getAuthHeaders(),
            body: formData,
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to upload CV.",
        );
    }

    return response.json();
}

export async function updateCv(
    cvId: number,
    payload: CvUpdatePayload,
): Promise<Cv> {
    const response = await fetch(
        `${API_BASE_URL}/cvs/${cvId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update CV.",
        );
    }

    return response.json();
}

export async function setDefaultCv(
    cvId: number,
): Promise<Cv> {
    const response = await fetch(
        `${API_BASE_URL}/cvs/${cvId}/set-default`,
        {
            method: "POST",
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to set default CV.",
        );
    }

    return response.json();
}

export async function deleteCv(
    cvId: number,
): Promise<Cv> {
    const response = await fetch(
        `${API_BASE_URL}/cvs/${cvId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to delete CV.",
        );
    }

    return response.json();
}

export function getCvDownloadUrl(
    cvId: number,
) {
    // NOTE: This URL is used for direct browser navigation/download
    // (e.g. an <a href> link). Browser navigation cannot attach an
    // Authorization header. Since the /cvs/{id}/download endpoint is
    // now ownership-protected (7.1.24.3.3), this download will fail
    // with 401 until this is addressed via a fetch+blob approach or
    // an alternative authenticated download mechanism.
    // Tracked as a known gap from the 7.1.24.5 Frontend Impact Review.
    return `${API_BASE_URL}/cvs/${cvId}/download`;
}

export async function getProfileEnrichmentProposals(
    profileId: number,
): Promise<ProfileEnrichmentProposal[]> {
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/enrichment`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load enrichment proposals.",
        );
    }

    return response.json();
}

export async function generateProfileEnrichment(
    cvId: number,
): Promise<ProfileEnrichmentProposal[]> {
    const response = await fetch(
        `${API_BASE_URL}/cvs/${cvId}/enrichment/generate`,
        {
            method: "POST",
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to generate enrichment proposals.",
        );
    }

    return response.json();
}

export async function acceptProfileEnrichment(
    proposalId: number,
    proposedValueOverride?: string,
    referenceId?: number,
): Promise<ProfileEnrichmentProposal> {
    const payload: AcceptProfileEnrichmentPayload = {};

    if (proposedValueOverride) {
        payload.proposed_value_override =
            proposedValueOverride;
    }

    if (referenceId !== undefined) {
        payload.reference_id = referenceId;
    }

    const hasPayload =
        Object.keys(payload).length > 0;

    const response = await fetch(
        `${API_BASE_URL}/enrichment/${proposalId}/accept`,
        {
            method: "POST",
            headers: {
                ...getAuthHeaders(),
                ...(hasPayload
                    ? {
                          "Content-Type": "application/json",
                      }
                    : {}),
            },
            ...(hasPayload
                ? {
                      body: JSON.stringify(payload),
                  }
                : {}),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to accept enrichment proposal.",
        );
    }

    return response.json();
}
export async function rejectProfileEnrichment(
    proposalId: number,
): Promise<ProfileEnrichmentProposal> {
    const response = await fetch(
        `${API_BASE_URL}/enrichment/${proposalId}/reject`,
        {
            method: "POST",
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to reject enrichment proposal.",
        );
    }

    return response.json();
}

export type JobDiscoverySettings = {
    discovery_enabled: boolean;
    discovery_interval_minutes: number;
    discovery_connectors: string[];
};

export type SearchCriteriaSettings = {
    target_job_titles: string[];
    preferred_countries: string[];
    work_modes: string[];
    included_keywords: string[];
    excluded_keywords: string[];
};

export type DiscoveryPreferencesSettings = {
    discovery_age_window: string;
    discovery_minimum_matching_score: number;
    discovery_show_archived: boolean;
    discovery_default_sort: string;
};

export type AISettings = {
    ai_features_enabled: boolean;
    ai_consent_accepted: boolean;
};

export type AISettingsUpdate = {
    ai_features_enabled: boolean;
    ai_consent_accepted: boolean;
};

export type AIContextPreview = {
    profile_id: number;
    is_ai_ready: boolean;
    missing_required_information: string[];
    available_categories: string[];
    missing_optional_categories: string[];
    excluded_categories: string[];
    ai_features_enabled: boolean;
    ai_consent_accepted: boolean;
    ai_call_allowed: boolean;
};

export type SavedSearch = {
    id: number;
    name: string;
    keyword: string;
    application_status: "ALL" | "APPLIED" | "NOT_APPLIED";
    source: string;
    location: string;
    sort_by: string;
};

export type SavedSearchCreate = {
    name: string;
    keyword: string;
    application_status: "ALL" | "APPLIED" | "NOT_APPLIED";
    source: string;
    location: string;
    sort_by: string;
};

export type ProfileOpportunityScore = {
  profile_id: number;
  profile_name: string;
  matching_score: number;
  skills_score: number;
  experience_score: number;
  work_mode_score: number;
  location_score: number;
  is_best_match: boolean;
}; 

export type Profile = {
    id: number;
    profile_name: string;
    full_name: string;
    current_title: string;
    location: string;
    years_of_experience: number;
    target_role_short_term: string;
    target_role_long_term: string;
    remote_preference: string;
    preferred_countries: string;
    professional_summary: string | null;
    career_motivations: string | null;
    preferred_environment: string | null;
    non_negotiables: string | null;
    additional_context: string | null;
    is_active: boolean;
    created_at: string;
    updated_at: string;
};


export async function getJobDiscoverySettings(
): Promise<JobDiscoverySettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/job-discovery`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load job discovery settings."
        );
    }

    return response.json();
}

export async function updateJobDiscoverySettings(
    payload: JobDiscoverySettings,
): Promise<JobDiscoverySettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/job-discovery`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update job discovery settings."
        );
    }

    return response.json();
}

export async function getSearchCriteriaSettings(
): Promise<SearchCriteriaSettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/search-criteria`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load search criteria settings."
        );
    }

    return response.json();
}

export async function updateSearchCriteriaSettings(
    payload: SearchCriteriaSettings,
): Promise<SearchCriteriaSettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/search-criteria`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update search criteria settings."
        );
    }

    return response.json();
}

export async function getDiscoveryPreferencesSettings(
): Promise<DiscoveryPreferencesSettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/discovery-preferences`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load discovery preferences."
        );
    }

    return response.json();
}

export async function getAISettings(
): Promise<AISettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/ai`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load AI settings."
        );
    }

    return response.json();
}

export async function updateAISettings(
    payload: AISettingsUpdate,
): Promise<AISettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/ai`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            await getApiErrorMessage(
                response,
                "Unable to update AI settings.",
            ),
        );
    }

    return response.json();
}

export async function getAIContextPreview(
    profileId: number,
): Promise<AIContextPreview> {
    // NOTE: The AI context router was not part of the 7.1.24.3
    // ownership migration audit. The Authorization header is added
    // here defensively, but backend ownership enforcement on this
    // endpoint has not been confirmed as of the 7.1.24.5 review.
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/ai-context-preview`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            await getApiErrorMessage(
                response,
                "Unable to load AI context preview.",
            ),
        );
    }

    return response.json();
}

export async function updateDiscoveryPreferencesSettings(
    payload: DiscoveryPreferencesSettings,
): Promise<DiscoveryPreferencesSettings> {
    const response = await fetch(
        `${API_BASE_URL}/settings/discovery-preferences`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update discovery preferences."
        );
    }

    return response.json();
}

export async function getSavedSearches(
): Promise<SavedSearch[]> {
    const response = await fetch(
        `${API_BASE_URL}/settings/saved-searches`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load saved searches."
        );
    }

    return response.json();
}

export async function createSavedSearch(
    payload: SavedSearchCreate,
): Promise<SavedSearch> {
    const response = await fetch(
        `${API_BASE_URL}/settings/saved-searches`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to create saved search."
        );
    }

    return response.json();
}

export async function deleteSavedSearch(
    savedSearchId: number,
): Promise<SavedSearch> {
    const response = await fetch(
        `${API_BASE_URL}/settings/saved-searches/${savedSearchId}`,
        {
            method: "DELETE",
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to delete saved search."
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
    // NOTE: The matching router was not part of the 7.1.24.3
    // ownership migration audit. The Authorization header is added
    // here defensively, but backend ownership enforcement on this
    // endpoint has not been confirmed as of the 7.1.24.5 review.
    const response = await fetch(
        `${API_BASE_URL}/matching/${profileId}/${jobOfferId}`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load matching result."
        );
    }

    return response.json();
}

export async function getProfileScoresForJobOffer(
    jobOfferId: number,
): Promise<ProfileOpportunityScore[]> {
    // NOTE: See getMatching() above regarding matching router
    // ownership status (not confirmed as of 7.1.24.5).
    const response = await fetch(
        `${API_BASE_URL}/matching/job-offers/${jobOfferId}/profiles`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load profile scores for job offer."
        );
    }

    return response.json();
}


export async function getRankedJobOffers(
    profileId: number,
) {
    // NOTE: See getMatching() above regarding matching router
    // ownership status (not confirmed as of 7.1.24.5).
    const response = await fetch(
        `${API_BASE_URL}/profiles/${profileId}/ranked-job-offers`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load ranked job offers."
        );
    }

    return response.json();
}

export type Application = {
    id: number;
    profile_id: number;
    job_offer_id: number;
    status: string;
    notes: string | null;
    source_type: string;
    created_at: string;
    updated_at: string;
};

export type ApplicationEvent = {
    id: number;
    application_id: number;
    event_type: string;
    old_value: string | null;
    new_value: string | null;
    event_date: string;
};

export async function getApplications() {
    const response = await fetch(
        `${API_BASE_URL}/applications`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load applications."
        );
    }

    return response.json();
}

export async function getApplicationTimeline(
    applicationId: number,
): Promise<ApplicationEvent[]> {
    const response = await fetch(
        `${API_BASE_URL}/applications/${applicationId}/timeline`,
        {
            headers: getAuthHeaders(),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load application timeline."
        );
    }

    return response.json();
}

export type ApplicationUpdatePayload = {
    profile_id: number;
    status: string;
    notes: string | null;
    source_type: string;
};

export type ApplicationStatusTransitionPayload = {
    status: string;
};

export type ApplicationCreatePayload = {
    profile_id: number;
    job_offer_id: number;
    status: string;
    notes: string | null;
    source_type: string;
};

export async function createApplication(
    payload: ApplicationCreatePayload,
): Promise<Application> {
    const response = await fetch(
        `${API_BASE_URL}/applications`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Unable to create application.",
        );
    }

    return response.json();
}

export async function updateApplication(
    applicationId: number,
    payload: ApplicationUpdatePayload,
): Promise<Application> {
    const response = await fetch(
        `${API_BASE_URL}/applications/${applicationId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            await getApiErrorMessage(
                response,
                "Unable to update application.",
            ),
        );
    }

    return response.json();
}

export async function changeApplicationStatus(
    applicationId: number,
    payload: ApplicationStatusTransitionPayload,
): Promise<Application> {
    const response = await fetch(
        `${API_BASE_URL}/applications/${applicationId}/status`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            await getApiErrorMessage(
                response,
                "Unable to change application status.",
            ),
        );
    }

    return response.json();
}

export async function createProfileCertification(
    payload: ProfileCertificationPayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-certifications`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to add profile certification."
        );
    }

    return response.json();
}

export async function updateProfileCertification(
    profileId: number,
    certificationId: number,
    payload: ProfileCertificationUpdatePayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-certifications/${profileId}/${certificationId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to update profile certification."
        );
    }

    return response.json();
}

export async function deleteProfileCertification(
    profileId: number,
    certificationId: number,
) {
    const response = await fetch(
        `${API_BASE_URL}/profile-certifications/${profileId}/${certificationId}`,
        {
            method: "DELETE",
            headers: getAuthHeaders(),
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to remove profile certification."
        );
    }

    return response.json();
}
