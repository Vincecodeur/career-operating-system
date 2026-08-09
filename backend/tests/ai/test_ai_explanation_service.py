from app.ai.exceptions import AIProviderError
from app.ai.providers.mock_provider import MockAIProvider
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse
from app.ai.services import AIExplanationService


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
            "The opportunity is aligned with backend API experience but "
            "requires stronger containerization skills."
        ),
    )


def _make_service(
    ai_enabled: bool = True,
) -> AIExplanationService:
    provider = MockAIProvider()

    return AIExplanationService(
        provider=provider,
        provider_name=provider.provider_name,
        model_name=provider.model_name,
        prompt_version="score_explanation_v1",
        ai_enabled=ai_enabled,
    )


def test_service_returns_explanation_with_valid_context():
    service = _make_service()

    result = service.generate_explanation(
        _make_context()
    )

    assert result.success is True
    assert result.explanation is not None
    assert result.error_message is None


def test_service_preserves_provider_metadata():
    service = _make_service()

    result = service.generate_explanation(
        _make_context()
    )

    assert result.explanation is not None
    assert result.explanation.provider_name == "mock"
    assert result.explanation.model_name == "mock-ai-explanation-model"
    assert result.explanation.prompt_version == "score_explanation_v1"


def test_service_returns_failure_when_disabled():
    service = _make_service(
        ai_enabled=False,
    )

    result = service.generate_explanation(
        _make_context()
    )

    assert result.success is False
    assert result.explanation is None
    assert result.error_message == "AI explanation disabled"


def test_service_does_not_modify_context_score():
    context = _make_context()
    original_score = context.score

    service = _make_service()

    service.generate_explanation(
        context
    )

    assert context.score == original_score


class FailingProvider(MockAIProvider):
    def generate_explanation(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        raise AIProviderError(
            "Fake provider error"
        )


def test_service_returns_failure_when_provider_fails():
    provider = FailingProvider()

    service = AIExplanationService(
        provider=provider,
        provider_name=provider.provider_name,
        model_name=provider.model_name,
        prompt_version="score_explanation_v1",
        ai_enabled=True,
    )

    result = service.generate_explanation(
        _make_context()
    )

    assert result.success is False
    assert result.explanation is None
    assert result.error_message == "AI explanation unavailable"