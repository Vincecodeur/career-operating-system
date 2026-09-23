from datetime import datetime
from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator


class AIExplanation(BaseModel):
    """
    Represents a validated AI explanation ready to be exposed
    by the API layer.

    The explanation does not compute or modify any business score.
    """

    summary: str = Field(
        min_length=20,
        max_length=1000,
    )

    detailed_explanation: str = Field(
        min_length=50,
        max_length=10000,
    )

    action_plan: list[str] = Field(
        default_factory=list,
        max_length=20,
    )

    generated_at: datetime

    provider_name: str = Field(
        min_length=1,
    )

    model_name: str = Field(
        min_length=1,
    )

    prompt_version: str = Field(
        min_length=1,
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class AIExplanationContext(BaseModel):
    """
    Represents the validated deterministic context sent to the
    AI explanation layer.

    This context must only contain already computed business data.
    """

    job_title: str = Field(
        min_length=1,
    )

    score: int = Field(
        ge=0,
        le=100,
    )

    strengths: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    weaknesses: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    recommendation: str = Field(
        min_length=1,
    )

    verdict: str = Field(
        min_length=1,
    )

    summary: str = Field(
        min_length=1,
    )

    # DEC-090 - Enriched AI Explanation Context. All optional, so
    # existing callers building a minimal v1-style context never
    # break. Each field maps to a category already listed as
    # available_categories in DEC-078 (HARD_SKILLS, WORK_EXPERIENCES,
    # ADDITIONAL_PROFILE_CONTEXT) - never RAW_CV, never unvalidated
    # data.
    matching_skills: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    missing_skills: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    relevant_experience_summary: str | None = None

    professional_summary: str | None = None

    career_motivations: str | None = None

    # DEC-092 - Full Profile Context In French. All optional, all
    # already-validated structured data (never raw CV text), all
    # already covered by DEC-078's available_categories
    # (CAREER_GOALS, ADDITIONAL_PROFILE_CONTEXT, SOFT_SKILLS,
    # LANGUAGES, CERTIFICATIONS).
    target_role_short_term: str | None = None

    target_role_long_term: str | None = None

    preferred_environment: str | None = None

    non_negotiables: str | None = None

    additional_context: str | None = None

    soft_skills: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    languages: list[str] = Field(
        default_factory=list,
        max_length=20,
    )

    certifications: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class AIProviderRequest(BaseModel):
    """
    Normalized request sent to an AI provider.
    """

    prompt: str = Field(
        min_length=1,
    )

    prompt_version: str = Field(
        min_length=1,
    )

    context: AIExplanationContext

    model_config = ConfigDict(
        extra="forbid",
    )


class AIProviderResponse(BaseModel):
    """
    Normalized response returned by an AI provider.
    """

    summary: str = Field(
        min_length=20,
        max_length=1000,
    )

    detailed_explanation: str = Field(
        min_length=50,
        max_length=10000,
    )

    action_plan: list[str] = Field(
        default_factory=list,
        max_length=20,
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class AIExplanationResult(BaseModel):
    """
    Result object returned by AIExplanationService.

    A failure must never break the deterministic matching flow.
    """

    success: bool

    explanation: AIExplanation | None = None

    error_message: str | None = None

    model_config = ConfigDict(
        extra="forbid",
    )

    @model_validator(
        mode="after",
    )
    def validate_result_consistency(
        self,
    ) -> Self:
        if self.success and self.explanation is None:
            raise ValueError(
                "A successful AIExplanationResult must include an explanation."
            )

        if self.success and self.error_message is not None:
            raise ValueError(
                "A successful AIExplanationResult must not include an error message."
            )

        if not self.success and self.explanation is not None:
            raise ValueError(
                "A failed AIExplanationResult must not include an explanation."
            )

        return self


class AIProviderConfiguration(BaseModel):
    """
    Represents the active AI provider configuration.
    """

    provider_name: str = Field(
        min_length=1,
    )

    model_name: str = Field(
        min_length=1,
    )

    timeout_seconds: int = Field(
        ge=1,
        le=300,
    )

    prompt_version: str = Field(
        min_length=1,
    )

    model_config = ConfigDict(
        extra="forbid",
    )