import json
import logging
import time

from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

logger = logging.getLogger(__name__)

# Extra retries applied on top of the SDK's own internal retry logic
# (tenacity, up to 5 attempts with exponential backoff on 408/429/
# 500/502/503/504), for transient errors that still fail after those
# internal retries are exhausted. Real incident observed 2026-09-22:
# a genuine 503 UNAVAILABLE ("high demand") from Gemini, unrelated to
# our own request volume. Kept intentionally short (2 extra attempts)
# since a sustained outage should simply defer the offer to the next
# scheduled run (DEC-089), not block the whole run indefinitely.
_TRANSIENT_RETRY_DELAYS_SECONDS = [10, 30]

from app.ai.exceptions import AIProviderAuthenticationError
from app.ai.exceptions import AIProviderConfigurationError
from app.ai.exceptions import AIProviderInvalidResponseError
from app.ai.exceptions import AIProviderTimeout
from app.ai.exceptions import AIProviderUnavailableError
from app.ai.interfaces import AIProvider
from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse


class _GeminiStructuredOutput(BaseModel):
    """
    Schema declared to Gemini's native structured output feature
    (response_mime_type="application/json" + response_schema).

    Kept deliberately separate from AIProviderResponse: this schema
    has no min/max length constraints, since Gemini's structured
    output enforces field presence and type, not string length. The
    stricter AIProviderResponse constraints are validated afterwards,
    in _parse_response(), where a violation is treated as an invalid
    response rather than a schema generation error.
    """

    summary: str
    detailed_explanation: str
    action_plan: list[str] = Field(default_factory=list)


class GeminiProvider(AIProvider):
    """
    Real AI provider backed by Google Gemini (google-genai SDK).

    Implements the existing AIProvider interface without modifying it
    (DEC-085). The SDK already retries transient errors (408, 429,
    500, 502, 503, 504) internally with exponential backoff; this
    provider only handles the final failure after those retries are
    exhausted.
    """

    provider_name = "gemini"

    def __init__(
        self,
        api_key: str,
        model_name: str,
        timeout_seconds: int,
    ):
        if not api_key:
            raise AIProviderConfigurationError(
                "GEMINI_API_KEY is not configured."
            )

        self.model_name = model_name
        self._client = genai.Client(api_key=api_key)
        self._timeout_seconds = timeout_seconds

    def generate_explanation(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        last_transient_error: (
            AIProviderUnavailableError | AIProviderTimeout | None
        ) = None

        attempts = len(_TRANSIENT_RETRY_DELAYS_SECONDS) + 1

        for attempt_index in range(attempts):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=request.prompt,
                    config=genai_types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=_GeminiStructuredOutput,
                    ),
                )
            except genai_errors.ClientError as error:
                if error.code in (401, 403):
                    raise AIProviderAuthenticationError(
                        str(error)
                    ) from error

                # 429 RESOURCE_EXHAUSTED and other 4xx transient cases
                last_transient_error = AIProviderUnavailableError(
                    str(error)
                )
            except genai_errors.ServerError as error:
                last_transient_error = AIProviderUnavailableError(
                    str(error)
                )
            except TimeoutError as error:
                last_transient_error = AIProviderTimeout(
                    str(error)
                )
            else:
                response_text = (response.text or "").strip()

                if not response_text:
                    raise AIProviderInvalidResponseError(
                        "Gemini returned an empty response."
                    )

                return self._parse_response(response_text)

            if attempt_index < len(_TRANSIENT_RETRY_DELAYS_SECONDS):
                delay = _TRANSIENT_RETRY_DELAYS_SECONDS[attempt_index]

                logger.warning(
                    "Transient Gemini error (%s), retrying in %s "
                    "second(s) (attempt %s/%s): %s",
                    type(last_transient_error).__name__,
                    delay,
                    attempt_index + 2,
                    attempts,
                    last_transient_error,
                )

                time.sleep(delay)

        raise last_transient_error

    @staticmethod
    def _parse_response(
        response_text: str,
    ) -> AIProviderResponse:
        """
        Parses Gemini's structured JSON output into the normalized
        AIProviderResponse contract.

        Confirmed by a real manual test with fictional data
        (2026-09-15): Gemini 3.1 Flash-Lite returns a JSON object
        matching _GeminiStructuredOutput even without an explicit
        schema constraint, sometimes wrapped in a markdown code fence
        (```json ... ```). The stripping below is kept as a defensive
        fallback even though response_schema/response_mime_type are
        now declared on the request, which should make Gemini return
        raw JSON directly per the SDK's structured output contract.
        """
        cleaned_text = response_text

        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.strip("`")
            cleaned_text = cleaned_text.removeprefix("json").strip()

        try:
            raw_payload = json.loads(cleaned_text)
        except json.JSONDecodeError as error:
            raise AIProviderInvalidResponseError(
                f"Gemini response is not valid JSON: {error}"
            ) from error

        try:
            structured_output = _GeminiStructuredOutput(
                **raw_payload
            )

            return AIProviderResponse(
                summary=structured_output.summary,
                detailed_explanation=(
                    structured_output.detailed_explanation
                ),
                action_plan=structured_output.action_plan,
            )
        except ValidationError as error:
            raise AIProviderInvalidResponseError(
                f"Gemini response does not match the expected "
                f"contract: {error}"
            ) from error