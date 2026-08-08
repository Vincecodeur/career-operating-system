from app.jobs.normalized_job_offer_schema import NormalizedJobOffer


def test_create_normalized_job_offer():
    job_offer = NormalizedJobOffer(
        title="Integration Architect",
        company="Test Company",
        description_raw="Integration Architect role",
        description_normalized="Integration Architect role",
        url_primary="https://example.com/jobs/123",
        language="EN",
        city="Paris",
        region="Ile-de-France",
        country="France",
        work_mode="HYBRID",
        contract_type="CDI",
        seniority="SENIOR",
        salary_min=70000,
        salary_max=90000,
        salary_currency="EUR",
        salary_original_text="70000 - 90000 EUR",
        skills_extracted=[
            "API",
            "Ecommerce",
        ],
        skills_normalized=[
            "API",
            "Ecommerce",
        ],
        quality_level="GOOD",
        status="ACTIVE",
    )

    assert job_offer.title == "Integration Architect"
    assert job_offer.company == "Test Company"
    assert job_offer.language == "EN"
    assert job_offer.country == "France"
    assert job_offer.work_mode == "HYBRID"
    assert job_offer.contract_type == "CDI"
    assert job_offer.seniority == "SENIOR"
    assert job_offer.salary_min == 70000
    assert job_offer.salary_max == 90000
    assert job_offer.salary_currency == "EUR"
    assert len(job_offer.skills_normalized) == 2
    assert job_offer.quality_level == "GOOD"
    assert job_offer.status == "ACTIVE"


def test_normalized_job_offer_allows_minimal_payload():
    job_offer = NormalizedJobOffer(
        title="Backend Developer",
        description_raw="Backend Developer role",
        url_primary="https://example.com/jobs/456",
        language="UNKNOWN",
        country="UNKNOWN",
        work_mode="UNKNOWN",
        contract_type="UNKNOWN",
        seniority="UNKNOWN",
        quality_level="PARTIAL",
    )

    assert job_offer.title == "Backend Developer"
    assert job_offer.country == "UNKNOWN"
    assert job_offer.work_mode == "UNKNOWN"
    assert job_offer.contract_type == "UNKNOWN"
    assert job_offer.seniority == "UNKNOWN"
    assert job_offer.quality_level == "PARTIAL"
    assert job_offer.status == "ACTIVE"