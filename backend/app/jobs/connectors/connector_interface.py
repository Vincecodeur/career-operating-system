from typing import Protocol
from typing import runtime_checkable

from app.jobs.raw_offer_schema import RawOffer


@runtime_checkable
class ConnectorInterface(Protocol):
    """
    Contrat commun à tous les connecteurs Job Discovery.

    Tout connecteur doit retourner une liste de RawOffer.
    """

    def fetch_job_offers(self) -> list[RawOffer]:
        ...