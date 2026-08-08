from app.core.database import SessionLocal
from app.jobs.discovery_service import DiscoveryService
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer
from app.jobs.connectors.mock_source_connector import MockSourceConnector


def cleanup_mock_source_data(db):
    db.query(JobOfferSource).filter(
        JobOfferSource.source_job_id.in_(
            [
                "MOCK-001",
                "MOCK-002",
            ]
        )
    ).delete()

    db.query(JobSource).filter(
        JobSource.name == "Mock Source"
    ).delete()

    db.query(JobOffer).filter(
        JobOffer.title.in_(
            [
                "Integration Architect",
                "Technical Program Manager",
            ]
        )
    ).delete()

    db.commit()


def test_end_to_end_pipeline_imports_mock_offers():
    db = SessionLocal()

    try:
        cleanup_mock_source_data(db)

        service = DiscoveryService(db)
        connector = MockSourceConnector()

        result = service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        assert result["source_name"] == "Mock Source"
        assert result["offers_fetched"] == 2
        assert result["offers_imported"] == 2

        job_offers = db.query(JobOffer).filter(
            JobOffer.title.in_(
                [
                    "Integration Architect",
                    "Technical Program Manager",
                ]
            )
        ).all()

        assert len(job_offers) == 2

    finally:
        cleanup_mock_source_data(db)
        db.close()


def test_end_to_end_pipeline_creates_job_sources():
    db = SessionLocal()

    try:
        cleanup_mock_source_data(db)

        service = DiscoveryService(db)
        connector = MockSourceConnector()

        service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        source = db.query(JobSource).filter(
            JobSource.name == "Mock Source"
        ).first()

        assert source is not None
        assert source.name == "Mock Source"

    finally:
        cleanup_mock_source_data(db)
        db.close()


def test_end_to_end_pipeline_creates_source_links():
    db = SessionLocal()

    try:
        cleanup_mock_source_data(db)

        service = DiscoveryService(db)
        connector = MockSourceConnector()

        service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        source_links = db.query(JobOfferSource).filter(
            JobOfferSource.source_job_id.in_(
                [
                    "MOCK-001",
                    "MOCK-002",
                ]
            )
        ).all()

        assert len(source_links) == 2

    finally:
        cleanup_mock_source_data(db)
        db.close()


def test_end_to_end_pipeline_prevents_duplicate_job_offers():
    db = SessionLocal()

    try:
        cleanup_mock_source_data(db)

        service = DiscoveryService(db)
        connector = MockSourceConnector()

        service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        job_offers = db.query(JobOffer).filter(
            JobOffer.title.in_(
                [
                    "Integration Architect",
                    "Technical Program Manager",
                ]
            )
        ).all()

        assert len(job_offers) == 2

    finally:
        cleanup_mock_source_data(db)
        db.close()


def test_end_to_end_pipeline_preserves_source_history():
    db = SessionLocal()

    try:
        cleanup_mock_source_data(db)

        service = DiscoveryService(db)
        connector = MockSourceConnector()

        service.import_from_connector(
            connector=connector,
            source_type="MOCK",
        )

        links = db.query(JobOfferSource).all()

        source_job_ids = {
            link.source_job_id
            for link in links
        }

        assert "MOCK-001" in source_job_ids
        assert "MOCK-002" in source_job_ids

    finally:
        cleanup_mock_source_data(db)
        db.close()