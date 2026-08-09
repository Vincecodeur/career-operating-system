import pytest

from app.ai.exceptions import AIError
from app.ai.exceptions import AIProviderAuthenticationError
from app.ai.exceptions import AIProviderConfigurationError
from app.ai.exceptions import AIProviderError
from app.ai.exceptions import AIProviderInvalidResponseError
from app.ai.exceptions import AIProviderTimeout
from app.ai.exceptions import AIProviderUnavailableError
from app.ai.exceptions import AIPromptBuildError
from app.ai.exceptions import AIPromptTemplateError
from app.ai.exceptions import AIValidationError


def test_ai_validation_error_inherits_ai_error():
    assert issubclass(
        AIValidationError,
        AIError,
    )


def test_provider_errors_inherit_provider_error():
    errors = [
        AIProviderTimeout,
        AIProviderConfigurationError,
        AIProviderAuthenticationError,
        AIProviderUnavailableError,
        AIProviderInvalidResponseError,
    ]

    for error in errors:
        assert issubclass(
            error,
            AIProviderError,
        )


def test_prompt_template_error_inherits_prompt_build_error():
    assert issubclass(
        AIPromptTemplateError,
        AIPromptBuildError,
    )


def test_can_raise_ai_provider_error():
    with pytest.raises(
        AIProviderError,
    ):
        raise AIProviderError(
            "provider error"
        )