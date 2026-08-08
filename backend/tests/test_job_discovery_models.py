from uuid import uuid4

from app.core.database import SessionLocal
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer


def test_create_job_discovery_models():
    db = SessionLocal()

    suffix = str(uuid4())

    job_offer = JobOffer(
        title=f"Integration Architect {suffix}",
        company_name="Test Company",
        location="Paris",
        city="Paris",
        region="Ile-de-France",
        country="France",
        source="Mock Source",
        source_url=f"https://example.com/jobs/{suffix}",
        url_primary=f"https://example.com/jobs/{suffix}",
        description="Integration Architect role with API and ecommerce scope.",
        description_raw="Integration Architect role with API and ecommerce scope.",
        language="EN",
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

    job_source = JobSource(
        name=f"Mock Source {suffix}",
        source_type="API",
        is_active=True,
    )

    try:
        db.add(job_offer)
        db.add(job_source)
        db.commit()

        db.refresh(job_offer)
        db.refresh(job_source)

        job_offer_source = JobOfferSource(
            job_offer_id=job_offer.id,
            job_source_id=job_source.id,
            source_job_id=f"mock-{suffix}",
            source_url=f"https://example.com/jobs/{suffix}",
        )

        db.add(job_offer_source)
        db.commit()
        db.refresh(job_offer_source)

        assert job_offer.id is not None
        assert job_offer.uuid is not None
        assert job_offer.title.startswith("Integration Architect")
        assert job_offer.country == "France"
        assert job_offer.work_mode == "HYBRID"
        assert job_offer.contract_type == "CDI"
        assert job_offer.quality_level == "GOOD"
        assert job_offer.status == "ACTIVE"

        assert job_source.id is not None
        assert job_source.uuid is not None
        assert job_source.source_type == "API"

        assert job_offer_source.id is not None
        assert job_offer_source.uuid is not None
        assert job_offer_source.job_offer_id == job_offer.id
        assert job_offer_source.job_source_id == job_source.id

    finally:
        db.rollback()
        db.query(JobOfferSource).filter(
            JobOfferSource.source_job_id == f"mock-{suffix}"
        ).delete()

        db.query(JobSource).filter(
            JobSource.name == f"Mock Source {suffix}"
        ).delete()

        db.query(JobOffer).filter(
            JobOffer.title == f"Integration Architect {suffix}"
        ).delete()

        db.commit()
        db.close()