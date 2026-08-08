from datetime import datetime

from app.jobs.raw_offer_schema import RawOffer


class MockSourceConnector:
    """
    Source simulée utilisée pour valider
    le pipeline Job Discovery.
    """

    SOURCE_NAME = "Mock Source"

    def fetch_job_offers(self) -> list[RawOffer]:
        return [
            RawOffer(
                source_name=self.SOURCE_NAME,
                source_job_id="MOCK-001",
                source_url="https://mock-source.local/jobs/001",
                title="Integration Architect",
                company="Example Company",
                raw_description=(
                    "Design and implement integrations using APIs "
                    "and cloud platforms."
                ),
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
                    "id": "MOCK-001"
                },
            ),
            RawOffer(
                source_name=self.SOURCE_NAME,
                source_job_id="MOCK-002",
                source_url="https://mock-source.local/jobs/002",
                title="Technical Program Manager",
                company="Example Company",
                raw_description=(
                    "Lead technical projects and coordinate teams."
                ),
                city="Lyon",
                region="Auvergne-Rhone-Alpes",
                country="France",
                contract_type_raw="CDI",
                work_mode_raw="Remote",
                salary_raw="65000 - 85000 EUR",
                published_at_raw="2026-08-08",
                language_raw="EN",
                retrieved_at=datetime.utcnow(),
                raw_payload={
                    "id": "MOCK-002"
                },
            ),
        ]