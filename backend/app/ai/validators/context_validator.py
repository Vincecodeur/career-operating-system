from app.ai.exceptions import AIValidationError
from app.ai.schemas import AIExplanationContext


class ContextValidator:
    """
    Validates deterministic context before any AI provider call.
    """

    @staticmethod
    def validate(
        context: AIExplanationContext,
    ) -> None:
        if context.score < 0 or context.score > 100:
            raise AIValidationError(
                "AI explanation context score must be between 0 and 100."
            )

        if not context.job_title:
            raise AIValidationError(
                "AI explanation context must include a job title."
            )

        if not context.recommendation:
            raise AIValidationError(
                "AI explanation context must include a recommendation."
            )

        if not context.verdict:
            raise AIValidationError(
                "AI explanation context must include a verdict."
            )

        if not isinstance(
            context.strengths,
            list,
        ):
            raise AIValidationError(
                "AI explanation context strengths must be a list."
            )

        if not isinstance(
            context.weaknesses,
            list,
        ):
            raise AIValidationError(
                "AI explanation context weaknesses must be a list."
            )