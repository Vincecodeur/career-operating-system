from datetime import datetime
from uuid import uuid4

from app.core.database import SessionLocal
from app.jobs.connectors.connector_registry import ConnectorRegistry
from app.jobs.discovery_service import DiscoveryService
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer
from app.jobs.raw_offer_schema import RawOffer


class FirstFakeConnector:
    suffix = ""

    def fetch_job_offers(
        self,
    ) -> list:
        return [
            RawOffer(
                source_name=f"First Source {self.suffix}",
                source_job_id=f"FIRST-{self.suffix}-001",
                source_url=f"https://example.com/first/{self.suffix}/001",
                title=f"Integration Architect {self.suffix}",
                company=f"Test Company {self.suffix}",
                raw_description="Integration Architect role from first source.",
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
                    "id": f"FIRST-{self.suffix}-001"
                },
            )
        ]


class SecondFakeConnector:
    suffix = ""

    def fetch_job_offers(
        self,
    ) -> list:
        return [
            RawOffer(
                source_name=f"Second Source {self.suffix}",
                source_job_id=f"SECOND-{self.suffix}-001",
                source_url=f"https://example.com/second/{self.suffix}/001",
                title=f"Integration Architect {self.suffix}",
                company=f"Test Company {self.suffix}",
                raw_description="Integration Architect role from second source.",
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
                    "id": f"SECOND-{self.suffix}-001"
                },
            )
        ]


def cleanup_test_data(
    db,
    suffix: str,
):
    db.query(JobOfferSource).filter(
        JobOfferSource.source_job_id.in_(
            [
                f"FIRST-{suffix}-001",
                f"SECOND-{suffix}-001",
            ]
        )
    ).delete()

    db.query(JobSource).filter(
        JobSource.name.in_(
            [
                f"First Source {suffix}",
                f"Second Source {suffix}",
            ]
        )
    ).delete()

    db.query(JobOffer).filter(
        JobOffer.title == f"Integration Architect {suffix}"
    ).delete()

    db.commit()


def test_import_from_connector_names_processes_multiple_connectors(
    monkeypatch,
):
    db = SessionLocal()
    suffix = str(uuid4())

    FirstFakeConnector.suffix = suffix
    SecondFakeConnector.suffix = suffix

    def fake_get_connector(
        connector_name: str,
    ):
        if connector_name == "first":
            return FirstFakeConnector

        if connector_name == "second":
            return SecondFakeConnector

        raise ValueError(
            f"Unknown connector: {connector_name}"
        )

    monkeypatch.setattr(
        ConnectorRegistry,
        "get_connector",
        fake_get_connector,
    )

    service = DiscoveryService(db)

    try:
        cleanup_test_data(
            db,
            suffix,
        )

        result = service.import_from_connector_names(
            connector_names=[
                "first",
                "second",
            ],
            source_type="MOCK",
        )

        assert result["connectors_processed"] == 2
        assert result["offers_fetched"] == 2
        assert result["offers_imported"] == 2
        assert len(result["results"]) == 2

    finally:
        db.rollback()
        cleanup_test_data(
            db,
            suffix,
        )
        db.close()


def test_multi_source_import_preserves_deduplication(
    monkeypatch,
):
    db = SessionLocal()
    suffix = str(uuid4())

    FirstFakeConnector.suffix = suffix
    SecondFakeConnector.suffix = suffix

    def fake_get_connector(
        connector_name: str,
    ):
        if connector_name == "first":
            return FirstFakeConnector

        if connector_name == "second":
            return SecondFakeConnector

        raise ValueError(
            f"Unknown connector: {connector_name}"
        )

    monkeypatch.setattr(
        ConnectorRegistry,
        "get_connector",
        fake_get_connector,
    )

    service = DiscoveryService(db)

    try:
        cleanup_test_data(
            db,
            suffix,
        )

        service.import_from_connector_names(
            connector_names=[
                "first",
                "second",
            ],
            source_type="MOCK",
        )

        job_offers = db.query(JobOffer).filter(
            JobOffer.title == f"Integration Architect {suffix}"
        ).all()

        assert len(job_offers) == 1

        source_links = db.query(JobOfferSource).filter(
            JobOfferSource.source_job_id.in_(
                [
                    f"FIRST-{suffix}-001",
                    f"SECOND-{suffix}-001",
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


def test_multi_source_import_creates_two_sources(
    monkeypatch,
):
    db = SessionLocal()
    suffix = str(uuid4())

    FirstFakeConnector.suffix = suffix
    SecondFakeConnector.suffix = suffix

    def fake_get_connector(
        connector_name: str,
    ):
        if connector_name == "first":
            return FirstFakeConnector

        if connector_name == "second":
            return SecondFakeConnector

        raise ValueError(
            f"Unknown connector: {connector_name}"
        )

    monkeypatch.setattr(
        ConnectorRegistry,
        "get_connector",
        fake_get_connector,
    )

    service = DiscoveryService(db)

    try:
        cleanup_test_data(
            db,
            suffix,
        )

        service.import_from_connector_names(
            connector_names=[
                "first",
                "second",
            ],
            source_type="MOCK",
        )

        sources = db.query(JobSource).filter(
            JobSource.name.in_(
                [
                    f"First Source {suffix}",
                    f"Second Source {suffix}",
                ]
            )
        ).all()

        assert len(sources) == 2

    finally:
        db.rollback()
        cleanup_test_data(
            db,
            suffix,
        )
        db.close()