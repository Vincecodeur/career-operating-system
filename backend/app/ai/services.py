from datetime import datetime
from datetime import timezone

from app.ai.exceptions import AIError
from app.ai.exceptions import AIProviderError
from app.ai.interfaces import AIProvider
from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.schemas import AIExplanation
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIExplanationResult
from app.ai.validators.context_validator import ContextValidator
from app.ai.validators.response_validator import ResponseValidator


class AIExplanationService:
    """
    Orchestrates AI explanation generation from deterministic inputs.

    This service does not calculate scores and does not depend on FastAPI,
    SQLAlchemy or any real LLM provider.
    """

    def __init__(
        self,
        provider: AIProvider,
        provider_name: str,
        model_name: str,
        prompt_version: str = "score_explanation_v1",
        ai_enabled: bool = True,
    ):
        self.provider = provider
        self.provider_name = provider_name
        self.model_name = model_name
        self.prompt_version = prompt_version
        self.ai_enabled = ai_enabled

    def generate_explanation(
        self,
        context: AIExplanationContext,
    ) -> AIExplanationResult:
        if not self.ai_enabled:
            return AIExplanationResult(
                success=False,
                explanation=None,
                error_message="AI explanation disabled",
            )

        try:
            ContextValidator.validate(
                context
            )

            request = PromptBuilder.build_request(
                context=context,
                prompt_version=self.prompt_version,
            )

            provider_response = self.provider.generate_explanation(
                request
            )

            ResponseValidator.validate(
                provider_response
            )

            explanation = AIExplanation(
                summary=provider_response.summary,
                detailed_explanation=provider_response.detailed_explanation,
                action_plan=provider_response.action_plan,
                generated_at=datetime.now(
                    timezone.utc
                ),
                provider_name=self.provider_name,
                model_name=self.model_name,
                prompt_version=self.prompt_version,
            )

            return AIExplanationResult(
                success=True,
                explanation=explanation,
                error_message=None,
            )

        except (
            AIError,
            AIProviderError,
            ValueError,
        ):
            return AIExplanationResult(
                success=False,
                explanation=None,
                error_message="AI explanation unavailable",
            )