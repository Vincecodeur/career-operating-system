from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from app.applications.models import Application
from app.core.database import SessionLocal
from app.jobs.job_offer_cleanup_service import delete_stale_job_offers
from app.jobs.job_offer_cleanup_service import find_stale_job_offer_ids
from app.jobs.job_offer_repository import JobOfferRepository
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer
from app.jobs.normalized_job_offer_schema import NormalizedJobOffer
from app.profile.models import Profile


def build_normalized_offer(suffix: str) -> NormalizedJobOffer:
    return NormalizedJobOffer(
        title=f"Cleanup Test Offer {suffix}",
        company=f"Cleanup Test Company {suffix}",
        description_raw="Offer used by the cleanup service test suite.",
        description_normalized="Offer used by the cleanup service test suite.",
        url_primary=f"https://example.com/cleanup/{suffix}",
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
        skills_extracted=["API"],
        skills_normalized=["API"],
        quality_level="GOOD",
        status="ACTIVE",
    )


def create_offer_with_last_seen_at(
    db,
    repository: JobOfferRepository,
    suffix: str,
    last_seen_at: datetime,
) -> JobOffer:
    """
    Creates a JobOffer with exactly one JobOfferSource, then forces
    last_seen_at to a controlled value so age-based staleness can be
    tested deterministically.
    """
    normalized_offer = build_normalized_offer(suffix)

    job_offer = repository.create_job_offer(
        normalized_offer=normalized_offer,
        source_name=f"Cleanup Mock Source {suffix}",
        source_type="API",
        source_job_id=f"cleanup-{suffix}",
        source_url=f"https://example.com/cleanup/{suffix}",
    )

    db.commit()
    db.refresh(job_offer)

    source_link = db.query(JobOfferSource).filter(
        JobOfferSource.job_offer_id == job_offer.id
    ).first()

    source_link.last_seen_at = last_seen_at
    db.commit()

    return job_offer


def cleanup_offer(db, suffix: str) -> None:
    db.query(Application).filter(
        Application.job_offer_id.in_(
            db.query(JobOffer.id).filter(
                JobOffer.title == f"Cleanup Test Offer {suffix}"
            )
        )
    ).delete(synchronize_session=False)

    db.query(JobOfferSource).filter(
        JobOfferSource.source_job_id == f"cleanup-{suffix}"
    ).delete()

    db.query(JobSource).filter(
        JobSource.name == f"Cleanup Mock Source {suffix}"
    ).delete()

    db.query(JobOffer).filter(
        JobOffer.title == f"Cleanup Test Offer {suffix}"
    ).delete()


def test_find_stale_job_offer_ids_returns_old_offers():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        old_offer = create_offer_with_last_seen_at(
            db,
            repository,
            suffix,
            datetime.utcnow() - timedelta(days=45),
        )

        stale_ids = find_stale_job_offer_ids(db, age_window_days=30)

        assert old_offer.id in stale_ids

    finally:
        db.rollback()
        cleanup_offer(db, suffix)
        db.commit()
        db.close()


def test_find_stale_job_offer_ids_excludes_recently_seen_offers():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        recent_offer = create_offer_with_last_seen_at(
            db,
            repository,
            suffix,
            datetime.utcnow() - timedelta(days=2),
        )

        stale_ids = find_stale_job_offer_ids(db, age_window_days=30)

        assert recent_offer.id not in stale_ids

    finally:
        db.rollback()
        cleanup_offer(db, suffix)
        db.commit()
        db.close()


def test_find_stale_job_offer_ids_excludes_offers_with_application():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        old_offer = create_offer_with_last_seen_at(
            db,
            repository,
            suffix,
            datetime.utcnow() - timedelta(days=45),
        )

        profile = db.query(Profile).filter(
            Profile.profile_name == "Test Primary Profile"
        ).first()

        application = Application(
            profile_id=profile.id,
            job_offer_id=old_offer.id,
            status="Applied",
            source_type="MANUAL",
        )
        db.add(application)
        db.commit()

        stale_ids = find_stale_job_offer_ids(db, age_window_days=30)

        assert old_offer.id not in stale_ids

    finally:
        db.rollback()
        cleanup_offer(db, suffix)
        db.commit()
        db.close()


def test_delete_stale_job_offers_removes_eligible_offers():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        old_offer = create_offer_with_last_seen_at(
            db,
            repository,
            suffix,
            datetime.utcnow() - timedelta(days=45),
        )
        old_offer_id = old_offer.id

        summary = delete_stale_job_offers(db, age_window_days=30)

        assert summary["deleted"] >= 1

        remaining = db.query(JobOffer).filter(
            JobOffer.id == old_offer_id
        ).first()

        assert remaining is None

    finally:
        db.rollback()
        cleanup_offer(db, suffix)
        db.commit()
        db.close()


def test_delete_stale_job_offers_preserves_offers_with_application():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        old_offer = create_offer_with_last_seen_at(
            db,
            repository,
            suffix,
            datetime.utcnow() - timedelta(days=45),
        )
        old_offer_id = old_offer.id

        profile = db.query(Profile).filter(
            Profile.profile_name == "Test Primary Profile"
        ).first()

        application = Application(
            profile_id=profile.id,
            job_offer_id=old_offer_id,
            status="Applied",
            source_type="MANUAL",
        )
        db.add(application)
        db.commit()

        summary = delete_stale_job_offers(db, age_window_days=30)

        assert summary["protected_by_application"] >= 1

        remaining = db.query(JobOffer).filter(
            JobOffer.id == old_offer_id
        ).first()

        assert remaining is not None

    finally:
        db.rollback()
        cleanup_offer(db, suffix)
        db.commit()
        db.close()


def test_delete_stale_job_offers_returns_accurate_summary():
    db = SessionLocal()
    repository = JobOfferRepository(db)
    suffix = str(uuid4())

    try:
        old_offer = create_offer_with_last_seen_at(
            db,
            repository,
            suffix,
            datetime.utcnow() - timedelta(days=45),
        )
        old_offer_id = old_offer.id

        expected_evaluated = db.query(JobOffer.id).count()
        expected_stale_ids = find_stale_job_offer_ids(
            db, age_window_days=30
        )

        # old_offer_id is captured above because delete_stale_job_offers()
        # commits the deletion, which expires all objects still attached
        # to this session. Accessing old_offer.id afterward would force
        # SQLAlchemy to reload a row that no longer exists, raising
        # ObjectDeletedError.
        summary = delete_stale_job_offers(db, age_window_days=30)

        assert summary["evaluated"] == expected_evaluated
        assert summary["deleted"] == len(expected_stale_ids)
        assert old_offer_id in expected_stale_ids
        assert isinstance(summary["protected_by_application"], int)

    finally:
        db.rollback()
        cleanup_offer(db, suffix)
        db.commit()
        db.close()
