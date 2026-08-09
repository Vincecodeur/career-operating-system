from app.ai.interfaces import AIProvider
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse


class FakeAIProvider(AIProvider):
    def generate_explanation(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        return AIProviderResponse(
            summary="This is a valid fake provider summary.",
            detailed_explanation=(
                "This fake provider returns a deterministic explanation "
                "that satisfies the schema validation constraints."
            ),
            action_plan=[
                "Review the deterministic weaknesses.",
            ],
        )


def test_fake_provider_implements_interface():
    provider = FakeAIProvider()

    assert isinstance(
        provider,
        AIProvider,
    )


def test_fake_provider_returns_response():
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

    provider = FakeAIProvider()

    response = provider.generate_explanation(
        request
    )

    assert isinstance(
        response,
        AIProviderResponse,
    )