from datetime import datetime
from uuid import uuid4

from app.core.database import SessionLocal
from app.jobs.discovery_service import DiscoveryService
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer
from app.jobs.raw_offer_schema import RawOffer


class TestConnector:
    def __init__(
        self,
        suffix: str,
    ):
        self.suffix = suffix
        self.source_name = f"Test Source {suffix}"

    def fetch_job_offers(
        self,
    ) -> list:
        return [
            RawOffer(
                source_name=self.source_name,
                source_job_id=f"TEST-{self.suffix}-001",
                source_url=f"https://example.com/jobs/{self.suffix}/001",
                title=f"Integration Architect {self.suffix}",
                company=f"Test Company {self.suffix}",
                raw_description="Integration Architect role with API scope.",
                city="Paris",
                region="Ile-de-France",
                country="France",
                contract_type_raw="CDI",
                work_mode_raw="HYBRID",
                salary_raw="70000 - 90000 EUR",
                published_at_raw="2026-08-08",
                language_raw="EN",
                retrieved_at=datetime.utcnow(),
                raw_payload={
                    "id": f"TEST-{self.suffix}-001"
                },
            ),
            RawOffer(
                source_name=self.source_name,
                source_job_id=f"TEST-{self.suffix}-002",
                source_url=f"https://example.com/jobs/{self.suffix}/002",
                title=f"Partner Integration Manager {self.suffix}",
                company=f"Test Company {self.suffix}",
                raw_description="Partner integration role with ecommerce scope.",
                city="Paris",
                region="Ile-de-France",
                country="France",
                contract_type_raw="CDI",
                work_mode_raw="HYBRID",
                salary_raw="75000 - 95000 EUR",
                published_at_raw="2026-08-08",
                language_raw="EN",
                retrieved_at=datetime.utcnow(),
                raw_payload={
                    "id": f"TEST-{self.suffix}-002"
                },
            ),
        ]


def cleanup_test_data(
    db,
    suffix: str,
):
    db.query(JobOfferSource).filter(
        JobOfferSource.source_job_id.in_(
            [
                f"TEST-{suffix}-001",
                f"TEST-{suffix}-002",
            ]
        )
    ).delete()

    db.query(JobSource).filter(
        JobSource.name == f"Test Source {suffix}"
    ).delete()

    db.query(JobOffer).filter(
        JobOffer.title.in_(
            [
                f"Integration Architect {suffix}",
                f"Partner Integration Manager {suffix}",
            ]
        )
    ).delete()

    db.commit()


def test_discovery_service_imports_offers_from_connector():
    db = SessionLocal()
    suffix = str(uuid4())
    connector = TestConnector(suffix)
    service = DiscoveryService(db)

    try:
        result = service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        assert result["source_name"] == f"Test Source {suffix}"
        assert result["offers_fetched"] == 2
        assert result["offers_imported"] == 2

        job_offers = db.query(JobOffer).filter(
            JobOffer.title.in_(
                [
                    f"Integration Architect {suffix}",
                    f"Partner Integration Manager {suffix}",
                ]
            )
        ).all()

        assert len(job_offers) == 2

    finally:
        db.rollback()
        cleanup_test_data(
            db,
            suffix,
        )
        db.close()


def test_discovery_service_creates_source_links():
    db = SessionLocal()
    suffix = str(uuid4())
    connector = TestConnector(suffix)
    service = DiscoveryService(db)

    try:
        service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        source_links = db.query(JobOfferSource).filter(
            JobOfferSource.source_job_id.in_(
                [
                    f"TEST-{suffix}-001",
                    f"TEST-{suffix}-002",
                ]
            )
        ).all()

        assert len(source_links) == 2

    finally:
        db.rollback()
        cleanup_test_data(
            db,
            suffix,
        )
        db.close()


def test_discovery_service_reuses_existing_offers_on_second_import():
    db = SessionLocal()
    suffix = str(uuid4())
    connector = TestConnector(suffix)
    service = DiscoveryService(db)

    try:
        first_result = service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        second_result = service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        assert first_result["offers_imported"] == 2
        assert second_result["offers_imported"] == 2

        job_offers = db.query(JobOffer).filter(
            JobOffer.title.in_(
                [
                    f"Integration Architect {suffix}",
                    f"Partner Integration Manager {suffix}",
                ]
            )
        ).all()

        assert len(job_offers) == 2

    finally:
        db.rollback()
        cleanup_test_data(
            db,
            suffix,
        )
        db.close()