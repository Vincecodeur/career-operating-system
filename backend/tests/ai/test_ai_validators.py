import pytest
from pydantic import ValidationError

from app.ai.exceptions import AIProviderInvalidResponseError
from app.ai.exceptions import AIValidationError
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderResponse
from app.ai.validators.context_validator import ContextValidator
from app.ai.validators.response_validator import ResponseValidator


def test_context_validator_accepts_valid_context():
    context = AIExplanationContext(
        job_title="Backend Engineer",
        score=78,
        strengths=[
            "Python",
        ],
        weaknesses=[
            "Docker",
        ],
        recommendation="APPLY",
        verdict="GOOD_MATCH",
        summary="Deterministic summary.",
    )

    ContextValidator.validate(
        context
    )


def test_context_validator_rejects_empty_job_title():
    with pytest.raises(
        ValidationError,
    ):
        AIExplanationContext(
            job_title="",
            score=78,
            strengths=[],
            weaknesses=[],
            recommendation="APPLY",
            verdict="GOOD_MATCH",
            summary="Deterministic summary.",
        )


def test_context_validator_rejects_empty_recommendation():
    with pytest.raises(
        ValidationError,
    ):
        AIExplanationContext(
            job_title="Backend Engineer",
            score=78,
            strengths=[],
            weaknesses=[],
            recommendation="",
            verdict="GOOD_MATCH",
            summary="Deterministic summary.",
        )


def test_context_validator_can_raise_validation_error_with_mutated_context():
    context = AIExplanationContext(
        job_title="Backend Engineer",
        score=78,
        strengths=[],
        weaknesses=[],
        recommendation="APPLY",
        verdict="GOOD_MATCH",
        summary="Deterministic summary.",
    )

    context.strengths = "invalid"

    with pytest.raises(
        AIValidationError,
    ):
        ContextValidator.validate(
            context
        )


def test_response_validator_accepts_valid_response():
    response = AIProviderResponse(
        summary="This is a valid response summary.",
        detailed_explanation=(
            "This is a valid detailed explanation that satisfies "
            "the minimum schema validation constraints."
        ),
        action_plan=[],
    )

    ResponseValidator.validate(
        response
    )


def test_response_validator_rejects_empty_summary():
    with pytest.raises(
        ValidationError,
    ):
        AIProviderResponse(
            summary="",
            detailed_explanation=(
                "This detailed explanation is long enough to pass validation."
            ),
            action_plan=[],
        )


def test_response_validator_can_raise_invalid_response_error():
    response = AIProviderResponse(
        summary="This is a valid response summary.",
        detailed_explanation=(
            "This is a valid detailed explanation that satisfies "
            "the minimum schema validation constraints."
        ),
        action_plan=[],
    )

    response.action_plan = "invalid"

    with pytest.raises(
        AIProviderInvalidResponseError,
    ):
        ResponseValidator.validate(
            response
        )
        
def test_validate_no_unlisted_companies_accepts_known_company():
    response = AIProviderResponse(
        summary="This is a valid AI generated summary.",
        detailed_explanation=(
            "The candidate worked at Cazoo Group as a senior manager, "
            "which is relevant experience for this role."
        ),
        action_plan=[
            "Highlight the Cazoo Group experience in the application.",
        ],
    )

    # Should not raise.
    ResponseValidator.validate_no_unlisted_companies(
        response,
        relevant_experience_summary=(
            "1. Senior Manager at Cazoo Group\n"
            "2. Technical Partnership Manager at Anchanto"
        ),
    )


def test_validate_no_unlisted_companies_rejects_deformed_name():
    # Reproduces the real 2026-09-22 production incident: Gemini
    # returned "Curve Group" when the actual, provided company name
    # was "Cazoo Group".
    response = AIProviderResponse(
        summary="This is a valid AI generated summary.",
        detailed_explanation=(
            "The candidate worked at Curve Group as a senior manager, "
            "which is relevant experience for this role."
        ),
        action_plan=[],
    )

    with pytest.raises(
        AIProviderInvalidResponseError,
    ):
        ResponseValidator.validate_no_unlisted_companies(
            response,
            relevant_experience_summary=(
                "1. Senior Manager at Cazoo Group\n"
                "2. Technical Partnership Manager at Anchanto"
            ),
        )


def test_validate_no_unlisted_companies_skips_when_summary_is_none():
    response = AIProviderResponse(
        summary="This is a valid AI generated summary.",
        detailed_explanation=(
            "The candidate worked at Some Unlisted Group, which is "
            "not mentioned anywhere in the provided context."
        ),
        action_plan=[],
    )

    # Should not raise: no relevant_experience_summary was provided,
    # so there is nothing to validate against.
    ResponseValidator.validate_no_unlisted_companies(
        response,
        relevant_experience_summary=None,
    )