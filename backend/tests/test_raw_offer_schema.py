from datetime import datetime

from app.jobs.raw_offer_schema import RawOffer


def test_create_raw_offer():
    raw_offer = RawOffer(
        source_name="France Travail",
        source_job_id="FT-12345",
        source_url="https://example.com/job/12345",
        title="Integration Architect",
        company="Test Company",
        raw_description="Architecture and API integration role.",
        city="Paris",
        region="Ile-de-France",
        country="France",
        contract_type_raw="CDI",
        work_mode_raw="Hybrid",
        salary_raw="70000 - 90000 EUR",
        published_at_raw="2026-08-08",
        language_raw="FR",
        retrieved_at=datetime.utcnow(),
        raw_payload={
            "external_id": "FT-12345"
        },
    )

    assert raw_offer.source_name == "France Travail"
    assert raw_offer.source_job_id == "FT-12345"
    assert raw_offer.title == "Integration Architect"
    assert raw_offer.company == "Test Company"
    assert raw_offer.city == "Paris"
    assert raw_offer.country == "France"
    assert raw_offer.contract_type_raw == "CDI"
    assert raw_offer.work_mode_raw == "Hybrid"
    assert raw_offer.salary_raw == "70000 - 90000 EUR"
    assert raw_offer.raw_payload["external_id"] == "FT-12345"


def test_raw_offer_allows_minimal_payload():
    raw_offer = RawOffer(
        source_name="Mock Source",
        title="Backend Developer",
        raw_description="Developer role",
        retrieved_at=datetime.utcnow(),
    )

    assert raw_offer.source_name == "Mock Source"
    assert raw_offer.title == "Backend Developer"
    assert raw_offer.raw_description == "Developer role"