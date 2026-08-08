from datetime import datetime

from app.jobs.normalization_service import NormalizationService
from app.jobs.raw_offer_schema import RawOffer
from app.jobs.normalized_job_offer_schema import NormalizedJobOffer


def test_normalize_returns_normalized_job_offer():
    service = NormalizationService()

    raw_offer = RawOffer(
        source_name="Mock Source",
        source_job_id="MOCK-001",
        source_url="https://example.com/jobs/001",
        title="Integration Architect",
        company="Example Company",
        raw_description="Integration Architect role",
        city="Paris",
        region="Ile-de-France",
        country="France",
        contract_type_raw="CDI",
        work_mode_raw="HYBRID",
        salary_raw="70000 - 90000 EUR",
        language_raw="EN",
        retrieved_at=datetime.utcnow(),
    )

    normalized_offer = service.normalize(raw_offer)

    assert isinstance(
        normalized_offer,
        NormalizedJobOffer,
    )


def test_normalize_copies_expected_fields():
    service = NormalizationService()

    raw_offer = RawOffer(
        source_name="Mock Source",
        source_job_id="MOCK-001",
        source_url="https://example.com/jobs/001",
        title="Integration Architect",
        company="Example Company",
        raw_description="Integration Architect role",
        city="Paris",
        region="Ile-de-France",
        country="France",
        contract_type_raw="CDI",
        work_mode_raw="HYBRID",
        salary_raw="70000 - 90000 EUR",
        language_raw="EN",
        retrieved_at=datetime.utcnow(),
    )

    normalized_offer = service.normalize(raw_offer)

    assert normalized_offer.title == "Integration Architect"
    assert normalized_offer.company == "Example Company"
    assert normalized_offer.url_primary == "https://example.com/jobs/001"
    assert normalized_offer.language == "EN"
    assert normalized_offer.country == "France"
    assert normalized_offer.work_mode == "HYBRID"
    assert normalized_offer.contract_type == "CDI"


def test_normalize_defaults_unknown_values():
    service = NormalizationService()

    raw_offer = RawOffer(
        source_name="Mock Source",
        title="Developer",
        raw_description="Developer role",
        retrieved_at=datetime.utcnow(),
    )

    normalized_offer = service.normalize(raw_offer)

    assert normalized_offer.language == "UNKNOWN"
    assert normalized_offer.country == "UNKNOWN"
    assert normalized_offer.work_mode == "UNKNOWN"
    assert normalized_offer.contract_type == "UNKNOWN"
    assert normalized_offer.seniority == "UNKNOWN"


def test_normalize_initializes_empty_skill_lists():
    service = NormalizationService()

    raw_offer = RawOffer(
        source_name="Mock Source",
        title="Developer",
        raw_description="Developer role",
        retrieved_at=datetime.utcnow(),
    )

    normalized_offer = service.normalize(raw_offer)

    assert normalized_offer.skills_extracted == []
    assert normalized_offer.skills_normalized == []


def test_normalize_sets_default_status_and_quality():
    service = NormalizationService()

    raw_offer = RawOffer(
        source_name="Mock Source",
        title="Developer",
        raw_description="Developer role",
        retrieved_at=datetime.utcnow(),
    )

    normalized_offer = service.normalize(raw_offer)

    assert normalized_offer.status == "ACTIVE"
    assert normalized_offer.quality_level == "PARTIAL"