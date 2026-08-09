import pytest

from app.ai.exceptions import AIPromptBuildError
from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest


def _make_context() -> AIExplanationContext:
    return AIExplanationContext(
        job_title="Backend Engineer",
        score=78,
        strengths=[
            "Python",
            "FastAPI",
        ],
        weaknesses=[
            "Docker",
            "Kubernetes",
        ],
        recommendation="APPLY",
        verdict="GOOD_MATCH",
        summary=(
            "The role is aligned with backend API experience but requires "
            "stronger containerization skills."
        ),
    )


def test_prompt_builder_creates_provider_request():
    request = PromptBuilder.build_request(
        context=_make_context(),
        prompt_version="score_explanation_v1",
    )

    assert isinstance(
        request,
        AIProviderRequest,
    )


def test_prompt_includes_score_recommendation_and_verdict():
    request = PromptBuilder.build_request(
        context=_make_context(),
    )

    assert "78" in request.prompt
    assert "APPLY" in request.prompt
    assert "GOOD_MATCH" in request.prompt


def test_prompt_includes_anti_hallucination_rules():
    request = PromptBuilder.build_request(
        context=_make_context(),
    )

    assert "Do not modify the score." in request.prompt
    assert "Do not invent skills." in request.prompt
    assert "Do not invent experience." in request.prompt


def test_prompt_includes_expected_output_format():
    request = PromptBuilder.build_request(
        context=_make_context(),
    )

    assert "Expected Output:" in request.prompt
    assert "summary" in request.prompt
    assert "detailed_explanation" in request.prompt
    assert "action_plan" in request.prompt


def test_prompt_builder_preserves_prompt_version():
    request = PromptBuilder.build_request(
        context=_make_context(),
        prompt_version="score_explanation_v1",
    )

    assert request.prompt_version == "score_explanation_v1"


def test_prompt_builder_rejects_unknown_prompt_version():
    with pytest.raises(
        AIPromptBuildError,
    ):
        PromptBuilder.build_request(
            context=_make_context(),
            prompt_version="unknown",
        )


def test_prompt_builder_does_not_mutate_context():
    context = _make_context()
    original_score = context.score

    PromptBuilder.build_request(
        context=context,
    )

    assert context.score == original_score