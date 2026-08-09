class AIError(Exception):
    """
    Base exception for the AI Explanation domain.
    """


class AIValidationError(AIError):
    """
    Raised when AI input or output validation fails.
    """


class AIProviderError(AIError):
    """
    Base exception for AI provider errors.
    """


class AIProviderTimeout(AIProviderError):
    """
    Raised when an AI provider call times out.
    """


class AIProviderConfigurationError(AIProviderError):
    """
    Raised when provider configuration is invalid.
    """


class AIProviderAuthenticationError(AIProviderError):
    """
    Raised when provider authentication fails.
    """


class AIProviderUnavailableError(AIProviderError):
    """
    Raised when the provider is unavailable.
    """


class AIProviderInvalidResponseError(AIProviderError):
    """
    Raised when the provider returns an invalid response.
    """


class AIPromptBuildError(AIError):
    """
    Raised when a prompt cannot be built.
    """


class AIPromptTemplateError(AIPromptBuildError):
    """
    Raised when a prompt template is invalid.
    """