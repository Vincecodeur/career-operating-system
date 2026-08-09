import pytest

from app.jobs.connectors.connector_registry import (
    ConnectorRegistry,
)
from app.jobs.connectors.france_travail_connector import (
    FranceTravailConnector,
)
from app.jobs.connectors.mock_source_connector import (
    MockSourceConnector,
)


def test_registry_returns_all_connectors():
    connectors = ConnectorRegistry.get_connectors()

    assert len(connectors) == 2


def test_registry_contains_mock_connector():
    connectors = ConnectorRegistry.get_connectors()

    assert "mock" in connectors
    assert connectors["mock"] is MockSourceConnector


def test_registry_contains_france_travail_connector():
    connectors = ConnectorRegistry.get_connectors()

    assert "france_travail" in connectors
    assert (
        connectors["france_travail"]
        is FranceTravailConnector
    )


def test_get_connector_returns_mock_connector():
    connector_class = ConnectorRegistry.get_connector(
        "mock"
    )

    assert connector_class is MockSourceConnector


def test_get_connector_returns_france_travail_connector():
    connector_class = ConnectorRegistry.get_connector(
        "france_travail"
    )

    assert connector_class is FranceTravailConnector


def test_get_connector_raises_for_unknown_connector():
    with pytest.raises(
        ValueError,
        match="Unknown connector",
    ):
        ConnectorRegistry.get_connector(
            "unknown"
        )