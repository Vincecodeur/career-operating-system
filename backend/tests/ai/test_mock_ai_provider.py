from app.ai.providers.mock_provider import MockAIProvider
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse


def _make_request() -> AIProviderRequest:
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

    return AIProviderRequest(
        prompt="Explain this result.",
        prompt_version="score_explanation_v1",
        context=context,
    )


def test_mock_ai_provider_returns_response():
    provider = MockAIProvider()

    response = provider.generate_explanation(
        _make_request()
    )

    assert isinstance(
        response,
        AIProviderResponse,
    )


def test_mock_ai_provider_is_deterministic():
    provider = MockAIProvider()

    first_response = provider.generate_explanation(
        _make_request()
    )

    second_response = provider.generate_explanation(
        _make_request()
    )

    assert first_response == second_response


def test_mock_ai_provider_has_provider_metadata():
    provider = MockAIProvider()

    assert provider.provider_name == "mock"
    assert provider.model_name == "mock-ai-explanation-model"