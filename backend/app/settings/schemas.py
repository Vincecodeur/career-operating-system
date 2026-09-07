from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import model_validator


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


class DiscoveryPreferencesSettingsResponse(
    BaseModel,
):
    discovery_age_window: str

    discovery_minimum_matching_score: int

    discovery_show_archived: bool

    discovery_default_sort: str


class DiscoveryPreferencesSettingsUpdate(
    BaseModel,
):
    discovery_age_window: str

    discovery_minimum_matching_score: int

    discovery_show_archived: bool

    discovery_default_sort: str


class AISettingsResponse(
    BaseModel,
):
    """
    Represents the persisted global AI activation and consent state.
    """

    ai_features_enabled: bool

    ai_consent_accepted: bool

    model_config = ConfigDict(
        extra="forbid",
    )


class AISettingsUpdate(
    BaseModel,
):
    """
    Represents an explicit AI settings update.

    AI features cannot be enabled without accepted consent.
    Disabling AI features also revokes consent.
    """

    ai_features_enabled: bool

    ai_consent_accepted: bool

    model_config = ConfigDict(
        extra="forbid",
    )

    @model_validator(
        mode="after",
    )
    def validate_consent_consistency(
        self,
    ) -> Self:
        if (
            self.ai_features_enabled
            and not self.ai_consent_accepted
        ):
            raise ValueError(
                "AI consent must be accepted before AI features can be enabled."
            )

        if (
            not self.ai_features_enabled
            and self.ai_consent_accepted
        ):
            raise ValueError(
                "AI consent cannot remain accepted when AI features are disabled."
            )

        return self

class LinkedInEmailSettingsResponse(
    BaseModel,
):
    """
    Represents the persisted LinkedIn email connector configuration.

    The app_password is never exposed here, neither in clear nor
    encrypted. is_configured indicates whether a password is
    currently stored, without revealing anything about its value.
    """

    imap_host: str | None

    imap_port: int | None

    email_address: str | None

    folder: str

    is_configured: bool

    model_config = ConfigDict(
        extra="forbid",
    )


class LinkedInEmailSettingsUpdate(
    BaseModel,
):
    """
    Represents an explicit LinkedIn email connector configuration
    update.

    app_password is received in clear over HTTPS and encrypted before
    being persisted. It is never logged and never echoed back by the
    API.
    """

    imap_host: str

    imap_port: int

    email_address: str

    app_password: str

    folder: str = "INBOX"

    model_config = ConfigDict(
        extra="forbid",
    )

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