from app.jobs.connectors.france_travail_connector import (
    FranceTravailConnector,
)
from app.jobs.connectors.linkedin_connector import (
    LinkedInConnector,
)
from app.jobs.connectors.mock_source_connector import (
    MockSourceConnector,
)


class ConnectorRegistry:
    """
    Registre central des connecteurs Job Discovery.

    Permet de récupérer les connecteurs disponibles
    sans que les consommateurs aient besoin de connaître
    leur implémentation concrète.
    """

    @staticmethod
    def get_connectors() -> dict:
        return {
            "mock": MockSourceConnector,
            "france_travail": FranceTravailConnector,
            "linkedin": LinkedInConnector,
        }

    @classmethod
    def get_connector(
        cls,
        connector_name: str,
    ):
        connectors = cls.get_connectors()

        if connector_name not in connectors:
            raise ValueError(
                f"Unknown connector: {connector_name}"
            )

        return connectors[connector_name]