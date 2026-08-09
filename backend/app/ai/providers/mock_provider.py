from app.ai.interfaces import AIProvider
from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse


class MockAIProvider(AIProvider):
    """
    Deterministic local provider used for tests and development.

    This provider does not call any external service.
    """

    provider_name = "mock"
    model_name = "mock-ai-explanation-model"

    def generate_explanation(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        return AIProviderResponse(
            summary=(
                "This opportunity is aligned with the provided deterministic "
                "matching result and can be reviewed using the existing score."
            ),
            detailed_explanation=(
                "The deterministic score indicates alignment based on the "
                "provided strengths, weaknesses, verdict and recommendation. "
                "This explanation does not modify the score or infer any "
                "additional information beyond the supplied context."
            ),
            action_plan=[
                "Review the listed weaknesses.",
                "Adapt the application material accordingly.",
                "Use the deterministic summary as the main decision support.",
            ],
        )