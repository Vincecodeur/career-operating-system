from abc import ABC
from abc import abstractmethod

from app.ai.schemas import AIProviderRequest
from app.ai.schemas import AIProviderResponse


class AIProvider(ABC):
    """
    Abstract interface for all AI providers.

    Business services must depend on this interface only,
    never on a concrete provider implementation.
    """

    @abstractmethod
    def generate_explanation(
        self,
        request: AIProviderRequest,
    ) -> AIProviderResponse:
        """
        Generate an AI explanation from a normalized provider request.
        """