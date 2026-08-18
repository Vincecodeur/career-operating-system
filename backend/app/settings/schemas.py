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