from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.connectors.mock_source_connector import MockSourceConnector


def test_mock_source_connector_implements_interface():
    connector = MockSourceConnector()

    assert isinstance(
        connector,
        ConnectorInterface,
    )


def test_interface_requires_fetch_job_offers():
    connector = MockSourceConnector()

    offers = connector.fetch_job_offers()

    assert isinstance(offers, list)
    assert len(offers) > 0


def test_interface_returns_rawoffer_instances():
    connector = MockSourceConnector()

    offers = connector.fetch_job_offers()

    assert all(
        hasattr(offer, "source_name")
        and hasattr(offer, "title")
        and hasattr(offer, "raw_description")
        for offer in offers
    )