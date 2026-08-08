from app.jobs.connectors.mock_source_connector import MockSourceConnector
from app.jobs.raw_offer_schema import RawOffer


def test_fetch_job_offers_returns_list():
    connector = MockSourceConnector()

    offers = connector.fetch_job_offers()

    assert isinstance(offers, list)
    assert len(offers) > 0


def test_fetch_job_offers_returns_raw_offers():
    connector = MockSourceConnector()

    offers = connector.fetch_job_offers()

    assert all(
        isinstance(offer, RawOffer)
        for offer in offers
    )


def test_first_offer_contains_expected_data():
    connector = MockSourceConnector()

    offers = connector.fetch_job_offers()

    first_offer = offers[0]

    assert first_offer.source_name == "Mock Source"
    assert first_offer.source_job_id == "MOCK-001"
    assert first_offer.title == "Integration Architect"
    assert first_offer.country == "France"


def test_connector_returns_multiple_offers():
    connector = MockSourceConnector()

    offers = connector.fetch_job_offers()

    assert len(offers) == 2

    ids = [
        offer.source_job_id
        for offer in offers
    ]

    assert "MOCK-001" in ids
    assert "MOCK-002" in ids