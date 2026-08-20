from pydantic import BaseModel


class JobDiscoverySettingsResponse(
    BaseModel,
):
    discovery_enabled: bool

    discovery_interval_minutes: int

    discovery_connectors: list[str]


class JobDiscoverySettingsUpdate(
    BaseModel,
):
    discovery_enabled: bool

    discovery_interval_minutes: int

    discovery_connectors: list[str]
    
    
class SearchCriteriaSettingsResponse(
    BaseModel,
):
    target_job_titles: list[str]

    preferred_countries: list[str]

    work_modes: list[str]

    included_keywords: list[str]

    excluded_keywords: list[str]


class SearchCriteriaSettingsUpdate(
    BaseModel,
):
    target_job_titles: list[str]

    preferred_countries: list[str]

    work_modes: list[str]

    included_keywords: list[str]

    excluded_keywords: list[str]
    
    
class DiscoveryPreferencesSettingsResponse(BaseModel):
    discovery_age_window: str
    discovery_minimum_matching_score: int
    discovery_show_archived: bool
    discovery_default_sort: str


class DiscoveryPreferencesSettingsUpdate(BaseModel):
    discovery_age_window: str
    discovery_minimum_matching_score: int
    discovery_show_archived: bool
    discovery_default_sort: str
    
    
class SavedSearch(
    BaseModel,
):
    id: int

    name: str

    keyword: str

    application_status: str

    source: str

    location: str

    sort_by: str


class SavedSearchCreate(
    BaseModel,
):
    name: str

    keyword: str

    application_status: str

    source: str

    location: str

    sort_by: str