from uuid import uuid4

from app.core.database import SessionLocal
from app.jobs.job_offer_repository import JobOfferRepository
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer
from app.jobs.normalized_job_offer_schema import NormalizedJobOffer


def build_normalized_offer(
    suffix: str,
) -> NormalizedJobOffer:
    return NormalizedJobOffer(
        title=f"Integration Architect {suffix}",
        company=f"Test Company {suffix}",
        description_raw="Integration Architect role with API scope.",
        description_normalized="Integration Architect role with API scope.",
        url_primary=f"https://example.com/jobs/{suffix}",
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


def test_create_job_offer_from_normalized_offer():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        normalized_offer = build_normalized_offer(suffix)

        job_offer = repository.create_job_offer(
            normalized_offer=normalized_offer,
            source_name=f"Mock Source {suffix}",
            source_type="API",
            source_job_id=f"mock-{suffix}",
            source_url=f"https://example.com/jobs/{suffix}",
        )

        db.commit()
        db.refresh(job_offer)

        assert job_offer.id is not None
        assert job_offer.title == f"Integration Architect {suffix}"
        assert job_offer.company_name == f"Test Company {suffix}"
        assert job_offer.city == "Paris"
        assert job_offer.country == "France"
        assert job_offer.work_mode == "HYBRID"
        assert job_offer.contract_type == "CDI"
        assert job_offer.quality_level == "GOOD"

        source_link = db.query(JobOfferSource).filter(
            JobOfferSource.job_offer_id == job_offer.id
        ).first()

        assert source_link is not None
        assert source_link.source_job_id == f"mock-{suffix}"

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


def test_upsert_job_offer_reuses_duplicate():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        normalized_offer = build_normalized_offer(suffix)

        first_job_offer = repository.upsert_job_offer(
            normalized_offer=normalized_offer,
            source_name=f"Mock Source {suffix}",
            source_type="API",
            source_job_id=f"mock-{suffix}-1",
            source_url=f"https://example.com/jobs/{suffix}/1",
        )

        db.commit()
        db.refresh(first_job_offer)

        second_job_offer = repository.upsert_job_offer(
            normalized_offer=normalized_offer,
            source_name=f"Mock Source {suffix}",
            source_type="API",
            source_job_id=f"mock-{suffix}-2",
            source_url=f"https://example.com/jobs/{suffix}/2",
        )

        db.commit()
        db.refresh(second_job_offer)

        assert first_job_offer.id == second_job_offer.id

        source_links = db.query(JobOfferSource).filter(
            JobOfferSource.job_offer_id == first_job_offer.id
        ).all()

        assert len(source_links) == 2

    finally:
        db.rollback()

        db.query(JobOfferSource).filter(
            JobOfferSource.source_job_id.in_(
                [
                    f"mock-{suffix}-1",
                    f"mock-{suffix}-2",
                ]
            )
        ).delete()

        db.query(JobSource).filter(
            JobSource.name == f"Mock Source {suffix}"
        ).delete()

        db.query(JobOffer).filter(
            JobOffer.title == f"Integration Architect {suffix}"
        ).delete()

        db.commit()
        db.close()


def test_get_or_create_source_reuses_existing_source():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        first_source = repository.get_or_create_source(
            source_name=f"Mock Source {suffix}",
            source_type="API",
        )

        db.commit()
        db.refresh(first_source)

        second_source = repository.get_or_create_source(
            source_name=f"Mock Source {suffix}",
            source_type="API",
        )

        assert first_source.id == second_source.id

    finally:
        db.rollback()

        db.query(JobSource).filter(
            JobSource.name == f"Mock Source {suffix}"
        ).delete()

        db.commit()
        db.close()