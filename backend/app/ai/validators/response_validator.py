import re

from app.ai.exceptions import AIProviderInvalidResponseError
from app.ai.schemas import AIProviderResponse


# Matches capitalized phrases ending in a common company-name
# suffix (Group, Bank, Inc, etc.), used as a best-effort heuristic
# to detect a specific hallucination pattern observed in production
# (DEC-091, 2026-09-22): a real company name deformed into a
# plausible-sounding but incorrect variant.
COMPANY_SUFFIX_PATTERN = re.compile(
    r"\b([A-Z][a-zA-Z&\-]*(?:\s+[A-Z][a-zA-Z&\-]*){0,3}\s+"
    r"(?:Group|Bank|Inc|Ltd|SAS|SA|Corp|Corporation|LLC))\b"
)



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

    @staticmethod
    def validate_no_unlisted_companies(
        response: AIProviderResponse,
        relevant_experience_summary: str | None,
    ) -> None:
        """
        Best-effort heuristic check (DEC-091, real incident
        2026-09-22): scans the generated text for capitalized
        phrases ending in a common company suffix and rejects the
        response if any such phrase does not appear verbatim in the
        structured relevant_experience_summary provided to the model.

        Important limitation, stated explicitly: this is NOT a
        guarantee against all hallucinations. It only targets the
        specific pattern observed in production (a real company name
        deformed into a plausible variant, e.g. "Cazoo Group" ->
        "Curve Group"). A fabricated name without one of the
        recognized suffixes would not be caught by this check.
        """
        if not relevant_experience_summary:
            return

        text_to_check = (
            response.detailed_explanation
            + " "
            + " ".join(response.action_plan)
        )

        candidates = COMPANY_SUFFIX_PATTERN.findall(text_to_check)

        for candidate in candidates:
            if candidate not in relevant_experience_summary:
                raise AIProviderInvalidResponseError(
                    f"AI response references a company name "
                    f"('{candidate}') not found in the provided "
                    f"relevant_experience_summary - possible "
                    f"hallucination, rejecting response."
                )