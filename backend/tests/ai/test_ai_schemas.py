from datetime import datetime
from datetime import timezone

import pytest
from pydantic import ValidationError

from app.ai.schemas import AIExplanation
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIExplanationResult
from app.ai.schemas import AIProviderConfiguration
from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse


def test_create_ai_explanation():
    explanation = AIExplanation(
        summary="This is a valid AI generated summary.",
        detailed_explanation=(
            "This is a valid detailed explanation with enough content "
            "to satisfy the minimum validation constraints."
        ),
        action_plan=[
            "Review weaknesses.",
        ],
        generated_at=datetime.now(
            timezone.utc
        ),
        provider_name="mock",
        model_name="mock-model",
        prompt_version="score_explanation_v1",
    )

    assert explanation.provider_name == "mock"
    assert explanation.prompt_version == "score_explanation_v1"


def test_ai_explanation_rejects_short_summary():
    with pytest.raises(
        ValidationError,
    ):
        AIExplanation(
            summary="Too short",
            detailed_explanation=(
                "This detailed explanation is long enough to pass validation."
            ),
            action_plan=[],
            generated_at=datetime.now(
                timezone.utc
            ),
            provider_name="mock",
            model_name="mock-model",
            prompt_version="v1",
        )


def test_create_ai_explanation_context():
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

    assert context.score == 78


def test_ai_explanation_context_rejects_invalid_score():
    with pytest.raises(
        ValidationError,
    ):
        AIExplanationContext(
            job_title="Backend Engineer",
            score=101,
            strengths=[],
            weaknesses=[],
            recommendation="APPLY",
            verdict="GOOD_MATCH",
            summary="Deterministic summary.",
        )


def test_create_ai_provider_request():
    context = AIExplanationContext(
        job_title="Backend Engineer",
        score=78,
        strengths=[],
        weaknesses=[],
        recommendation="APPLY",
        verdict="GOOD_MATCH",
        summary="Deterministic summary.",
    )

    request = AIProviderRequest(
        prompt="Explain this result.",
        prompt_version="score_explanation_v1",
        context=context,
    )

    assert request.context.job_title == "Backend Engineer"


def test_create_ai_provider_response():
    response = AIProviderResponse(
        summary="This is a valid provider summary.",
        detailed_explanation=(
            "This is a valid provider detailed explanation with enough "
            "content to pass schema validation."
        ),
        action_plan=[
            "Review the weaknesses.",
        ],
    )

    assert response.action_plan == [
        "Review the weaknesses.",
    ]


def test_ai_explanation_result_success_requires_explanation():
    with pytest.raises(
        ValidationError,
    ):
        AIExplanationResult(
            success=True,
            explanation=None,
            error_message=None,
        )


def test_ai_explanation_result_failure_allows_error_message():
    result = AIExplanationResult(
        success=False,
        explanation=None,
        error_message="AI explanation unavailable",
    )

    assert result.success is False


def test_create_ai_provider_configuration():
    configuration = AIProviderConfiguration(
        provider_name="mock",
        model_name="mock-model",
        timeout_seconds=10,
        prompt_version="score_explanation_v1",
    )

    assert configuration.timeout_seconds == 10