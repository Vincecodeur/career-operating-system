from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class AIContextPreviewResponse(BaseModel):
    """
    Represents the context categories and readiness information
    available before any AI provider call.

    This schema never contains raw CV content, pending enrichment
    proposals, application history, secrets or provider prompts.
    """

    profile_id: int = Field(
        ge=1,
    )

    is_ai_ready: bool

    missing_required_information: list[str] = Field(
        default_factory=list,
    )

    available_categories: list[str] = Field(
        default_factory=list,
    )

    missing_optional_categories: list[str] = Field(
        default_factory=list,
    )

    excluded_categories: list[str] = Field(
        default_factory=list,
    )

    ai_features_enabled: bool

    ai_consent_accepted: bool

    ai_call_allowed: bool

    model_config = ConfigDict(
        extra="forbid",
    )