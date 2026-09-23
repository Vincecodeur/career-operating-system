from app.ai.exceptions import AIPromptBuildError
from app.ai.prompts.prompt_templates import PROMPT_TEMPLATES
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest
from app.ai.validators.context_validator import ContextValidator


# DEC-092 - score_explanation_v3 is written in French, so its
# required safety fragments differ from v1/v2 (English). Each prompt
# version must define its own list of mandatory anti-hallucination
# instructions, checked verbatim after rendering.
REQUIRED_FRAGMENTS_BY_VERSION = {
    "score_explanation_v1": [
        "Do not modify the score.",
        "Do not modify the verdict.",
        "Do not modify the recommendation.",
        "Do not invent skills.",
        "Do not invent experience.",
        "Expected Output:",
    ],
    "score_explanation_v2": [
        "Do not modify the score.",
        "Do not modify the verdict.",
        "Do not modify the recommendation.",
        "Do not invent skills.",
        "Do not invent experience.",
        "Expected Output:",
    ],
    "score_explanation_v3": [
        "Ne modifie jamais le score.",
        "Ne modifie jamais le verdict.",
        "Ne modifie jamais la recommandation.",
        "N'invente jamais de compétence.",
        "N'invente jamais d'expérience.",
        "Format de sortie attendu :",
    ],
}


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
            matching_skills=(
                ", ".join(context.matching_skills)
                if context.matching_skills
                else "Not specified"
            ),
            missing_skills=(
                ", ".join(context.missing_skills)
                if context.missing_skills
                else "Not specified"
            ),
            relevant_experience_summary=(
                context.relevant_experience_summary
                or "Non renseigné"
            ),
            professional_summary=(
                context.professional_summary or "Non renseigné"
            ),
            career_motivations=(
                context.career_motivations or "Non renseigné"
            ),
            target_role_short_term=(
                context.target_role_short_term or "Non renseigné"
            ),
            target_role_long_term=(
                context.target_role_long_term or "Non renseigné"
            ),
            preferred_environment=(
                context.preferred_environment or "Non renseigné"
            ),
            non_negotiables=(
                context.non_negotiables or "Non renseigné"
            ),
            additional_context=(
                context.additional_context or "Non renseigné"
            ),
            soft_skills=(
                ", ".join(context.soft_skills)
                if context.soft_skills
                else "Non renseigné"
            ),
            languages=(
                ", ".join(context.languages)
                if context.languages
                else "Non renseigné"
            ),
            certifications=(
                ", ".join(context.certifications)
                if context.certifications
                else "Non renseigné"
            ),
        ).strip()

        PromptBuilder._validate_prompt(
            prompt,
            prompt_version,
        )

        return AIProviderRequest(
            prompt=prompt,
            prompt_version=prompt_version,
            context=context,
        )

    @staticmethod
    def _validate_prompt(
        prompt: str,
        prompt_version: str,
    ) -> None:
        if not prompt:
            raise AIPromptBuildError(
                "Generated prompt cannot be empty."
            )

        required_fragments = REQUIRED_FRAGMENTS_BY_VERSION.get(
            prompt_version,
            [],
        )

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