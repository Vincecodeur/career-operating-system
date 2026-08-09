from app.ai.exceptions import AIPromptBuildError
from app.ai.prompts.prompt_templates import PROMPT_TEMPLATES
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest
from app.ai.validators.context_validator import ContextValidator


FORBIDDEN_PROMPT_SUBSTRINGS = [
    "FRANCE_TRAVAIL_CLIENT_SECRET",
    "FRANCE_TRAVAIL_CLIENT_ID",
    "DATABASE_URL",
    "JWT_SECRET",
    "API_KEY",
    "TOKEN",
    "PASSWORD",
]


class PromptBuilder:
    """
    Builds deterministic prompts from validated AIExplanationContext.

    The builder does not call any provider.
    """

    @staticmethod
    def build_request(
        context: AIExplanationContext,
        prompt_version: str = "score_explanation_v1",
    ) -> AIProviderRequest:
        ContextValidator.validate(
            context
        )

        template = PROMPT_TEMPLATES.get(
            prompt_version
        )

        if template is None:
            raise AIPromptBuildError(
                f"Unknown prompt version: {prompt_version}"
            )

        prompt = template.format(
            job_title=context.job_title,
            score=context.score,
            strengths=", ".join(
                context.strengths
            ),
            weaknesses=", ".join(
                context.weaknesses
            ),
            recommendation=context.recommendation,
            verdict=context.verdict,
            deterministic_summary=context.summary,
        ).strip()

        PromptBuilder._validate_prompt(
            prompt
        )

        return AIProviderRequest(
            prompt=prompt,
            prompt_version=prompt_version,
            context=context,
        )

    @staticmethod
    def _validate_prompt(
        prompt: str,
    ) -> None:
        if not prompt:
            raise AIPromptBuildError(
                "Generated prompt cannot be empty."
            )

        required_fragments = [
            "Do not modify the score.",
            "Do not modify the verdict.",
            "Do not modify the recommendation.",
            "Do not invent skills.",
            "Do not invent experience.",
            "Expected Output:",
        ]

        for fragment in required_fragments:
            if fragment not in prompt:
                raise AIPromptBuildError(
                    f"Generated prompt is missing required fragment: {fragment}"
                )

        upper_prompt = prompt.upper()

        for forbidden in FORBIDDEN_PROMPT_SUBSTRINGS:
            if forbidden in upper_prompt:
                raise AIPromptBuildError(
                    "Generated prompt contains a forbidden sensitive marker."
                )