from sqlalchemy.orm import Session

from app.jobs.connectors.connector_registry import ConnectorRegistry
from app.jobs.connectors.credentials_resolver import (
    CREDENTIAL_RESOLVERS,
)
from app.jobs.job_offer_repository import JobOfferRepository
from app.jobs.normalization_service import NormalizationService


class DiscoveryService:
    """
    Orchestre le pipeline Job Discovery.

    Flux :
    Connector
    -> RawOffer
    -> NormalizationService
    -> NormalizedJobOffer
    -> JobOfferRepository
    -> Database
    """

    def __init__(self, db: Session):
        self.db = db
        self.normalization_service = NormalizationService()
        self.job_offer_repository = JobOfferRepository(db)

    def import_from_connector(
        self,
        connector,
        source_type: str = "MANUAL",
    ) -> dict:
        raw_offers = connector.fetch_job_offers()

        imported_offers = []

        for raw_offer in raw_offers:
            normalized_offer = self.normalization_service.normalize(
                raw_offer
            )

            job_offer = self.job_offer_repository.upsert_job_offer(
                normalized_offer=normalized_offer,
                source_name=raw_offer.source_name,
                source_type=source_type,
                source_job_id=raw_offer.source_job_id,
                source_url=raw_offer.source_url,
            )

            imported_offers.append(job_offer)

        self.db.commit()

        return {
            "source_name": self._get_source_name(raw_offers),
            "offers_fetched": len(raw_offers),
            "offers_imported": len(imported_offers),
        }

    def import_from_connector_names(
        self,
        connector_names: list[str],
        source_type: str = "MANUAL",
        user_id: int | None = None,
    ) -> dict:
        import_results = []

        total_offers_fetched = 0
        total_offers_imported = 0

        connectors_skipped = 0

        for connector_name in connector_names:
            connector_class = ConnectorRegistry.get_connector(
                connector_name
            )

            resolver = CREDENTIAL_RESOLVERS.get(connector_name)

            if resolver is not None:
                if user_id is None:
                    # a connector requiring per-user credentials was
                    # requested, but no user context was provided:
                    # skip it silently rather than instantiate it
                    # without any credentials
                    connectors_skipped += 1
                    continue

                credentials = resolver(self.db, user_id)

                if credentials is None:
                    # connector enabled in discovery_connectors but
                    # not configured (or undecryptable) for this
                    # user: skip it silently, other connectors must
                    # still run normally
                    connectors_skipped += 1
                    continue

                connector = connector_class(**credentials)
            else:
                connector = connector_class()

            result = self.import_from_connector(
                connector=connector,
                source_type=source_type,
            )

            import_results.append(
                {
                    "connector_name": connector_name,
                    "source_name": result["source_name"],
                    "offers_fetched": result["offers_fetched"],
                    "offers_imported": result["offers_imported"],
                }
            )

            total_offers_fetched += result["offers_fetched"]
            total_offers_imported += result["offers_imported"]

        return {
            "connectors_processed": len(connector_names)
            - connectors_skipped,
            "connectors_skipped": connectors_skipped,
            "offers_fetched": total_offers_fetched,
            "offers_imported": total_offers_imported,
            "results": import_results,
        }

    @staticmethod
    def _get_source_name(
        raw_offers,
    ) -> str:
        if not raw_offers:
            return "UNKNOWN"

        return raw_offers[0].source_name