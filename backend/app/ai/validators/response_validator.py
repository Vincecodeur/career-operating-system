from app.ai.exceptions import AIProviderInvalidResponseError
from app.ai.schemas import AIProviderResponse


class ResponseValidator:
    """
    Validates normalized AI provider responses.
    """

    @staticmethod
    def validate(
        response: AIProviderResponse,
    ) -> None:
        if not response.summary:
            raise AIProviderInvalidResponseError(
                "AI provider response must include a summary."
            )

        if not response.detailed_explanation:
            raise AIProviderInvalidResponseError(
                "AI provider response must include a detailed explanation."
            )

        if not isinstance(
            response.action_plan,
            list,
        ):
            raise AIProviderInvalidResponseError(
                "AI provider response action plan must be a list."
            )