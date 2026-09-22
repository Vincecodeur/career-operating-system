import json
from types import SimpleNamespace

import pytest
from google.genai import errors as genai_errors

from app.ai.exceptions import AIProviderAuthenticationError
from app.ai.exceptions import AIProviderConfigurationError
from app.ai.exceptions import AIProviderInvalidResponseError
from app.ai.exceptions import AIProviderUnavailableError
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.schemas import AIExplanationContext
from app.ai.schemas import AIProviderRequest


def build_request() -> AIProviderRequest:
    context = AIExplanationContext(
        job_title="Backend Engineer",
        score=78,
        strengths=["Python"],
        weaknesses=["Docker"],
        recommendation="APPLY",
        verdict="GOOD_MATCH",
        summary="Deterministic summary.",
    )

    return AIProviderRequest(
        prompt="Explain this result.",
        prompt_version="score_explanation_v2",
        context=context,
    )


def build_provider() -> GeminiProvider:
    return GeminiProvider(
        api_key="fake-test-api-key",
        model_name="gemini-3.1-flash-lite",
        timeout_seconds=30,
    )


def fake_response(payload: dict) -> SimpleNamespace:
    return SimpleNamespace(
        text=json.dumps(payload)
    )


VALID_PAYLOAD = {
    "summary": "This is a valid AI generated summary.",
    "detailed_explanation": (
        "This is a valid detailed explanation with enough content "
        "to satisfy the minimum validation constraints."
    ),
    "action_plan": [
        "Review the weaknesses.",
    ],
}


def test_provider_raises_configuration_error_without_api_key():
    with pytest.raises(AIProviderConfigurationError):
        GeminiProvider(
            api_key="",
            model_name="gemini-3.1-flash-lite",
            timeout_seconds=30,
        )


def test_generate_explanation_returns_valid_response(monkeypatch):
    provider = build_provider()

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        lambda **kwargs: fake_response(VALID_PAYLOAD),
    )

    result = provider.generate_explanation(build_request())

    assert result.summary == VALID_PAYLOAD["summary"]
    assert (
        result.detailed_explanation
        == VALID_PAYLOAD["detailed_explanation"]
    )
    assert result.action_plan == VALID_PAYLOAD["action_plan"]


def test_generate_explanation_strips_markdown_fence(monkeypatch):
    provider = build_provider()

    fenced_text = (
        "```json\n" + json.dumps(VALID_PAYLOAD) + "\n```"
    )

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        lambda **kwargs: SimpleNamespace(text=fenced_text),
    )

    result = provider.generate_explanation(build_request())

    assert result.summary == VALID_PAYLOAD["summary"]


def test_generate_explanation_raises_on_empty_response(monkeypatch):
    provider = build_provider()

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        lambda **kwargs: SimpleNamespace(text=""),
    )

    with pytest.raises(AIProviderInvalidResponseError):
        provider.generate_explanation(build_request())


def test_generate_explanation_raises_on_malformed_json(monkeypatch):
    provider = build_provider()

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        lambda **kwargs: SimpleNamespace(text="not valid json"),
    )

    with pytest.raises(AIProviderInvalidResponseError):
        provider.generate_explanation(build_request())


def test_generate_explanation_raises_on_schema_mismatch(monkeypatch):
    provider = build_provider()

    incomplete_payload = {
        "summary": "Missing the other required fields.",
    }

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        lambda **kwargs: fake_response(incomplete_payload),
    )

    with pytest.raises(AIProviderInvalidResponseError):
        provider.generate_explanation(build_request())


def test_generate_explanation_maps_401_to_authentication_error(
    monkeypatch,
):
    provider = build_provider()

    def raise_401(**kwargs):
        raise genai_errors.ClientError(
            code=401,
            response_json={
                "error": {"message": "invalid api key"}
            },
        )

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        raise_401,
    )

    with pytest.raises(AIProviderAuthenticationError):
        provider.generate_explanation(build_request())


def test_generate_explanation_maps_403_to_authentication_error(
    monkeypatch,
):
    provider = build_provider()

    def raise_403(**kwargs):
        raise genai_errors.ClientError(
            code=403,
            response_json={
                "error": {"message": "permission denied"}
            },
        )

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        raise_403,
    )

    with pytest.raises(AIProviderAuthenticationError):
        provider.generate_explanation(build_request())


def test_generate_explanation_maps_429_to_unavailable_error(
    monkeypatch,
):
    provider = build_provider()

    monkeypatch.setattr(
        "app.ai.providers.gemini_provider.time.sleep",
        lambda seconds: None,
    )

    def raise_429(**kwargs):
        raise genai_errors.ClientError(
            code=429,
            response_json={
                "error": {"message": "quota exceeded"}
            },
        )

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        raise_429,
    )

    with pytest.raises(AIProviderUnavailableError):
        provider.generate_explanation(build_request())


def test_generate_explanation_retries_transient_error_then_succeeds(
    monkeypatch,
):
    provider = build_provider()

    monkeypatch.setattr(
        "app.ai.providers.gemini_provider.time.sleep",
        lambda seconds: None,
    )

    call_count = {"value": 0}

    def flaky_generate_content(**kwargs):
        call_count["value"] += 1

        if call_count["value"] == 1:
            raise genai_errors.ServerError(
                code=503,
                response_json={
                    "error": {"message": "high demand"}
                },
            )

        return fake_response(VALID_PAYLOAD)

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        flaky_generate_content,
    )

    result = provider.generate_explanation(build_request())

    assert result.summary == VALID_PAYLOAD["summary"]
    assert call_count["value"] == 2


def test_generate_explanation_exhausts_retries_and_raises(
    monkeypatch,
):
    provider = build_provider()

    monkeypatch.setattr(
        "app.ai.providers.gemini_provider.time.sleep",
        lambda seconds: None,
    )

    def always_raise_503(**kwargs):
        raise genai_errors.ServerError(
            code=503,
            response_json={
                "error": {"message": "high demand"}
            },
        )

    monkeypatch.setattr(
        provider._client.models,
        "generate_content",
        always_raise_503,
    )

    with pytest.raises(AIProviderUnavailableError):
        provider.generate_explanation(build_request())
