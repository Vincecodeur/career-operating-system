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