from datetime import datetime

import httpx

from app.core.settings import settings
from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.raw_offer_schema import RawOffer


class FranceTravailConnector(ConnectorInterface):
    """
    Connecteur France Travail pour récupérer des offres d'emploi
    depuis l'API officielle Offres d'emploi v2.

    API utilisée :
    - OAuth2 Client Credentials
    - GET /v2/offres/search
    """

    SOURCE_NAME = "France Travail"
    DEFAULT_SCOPE = "o2dsoffre api_offresdemploiv2"

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        token_url: str | None = None,
        api_url: str | None = None,
        timeout: int = 10,
    ):
        self.client_id = client_id or settings.FRANCE_TRAVAIL_CLIENT_ID
        self.client_secret = (
            client_secret
            or settings.FRANCE_TRAVAIL_CLIENT_SECRET
        )
        self.token_url = (
            token_url
            or settings.FRANCE_TRAVAIL_TOKEN_URL
        )
        self.api_url = (
            api_url
            or settings.FRANCE_TRAVAIL_API_URL
        )
        self.timeout = timeout

    def fetch_access_token(self) -> str:
        response = httpx.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": self.DEFAULT_SCOPE,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        payload = response.json()

        return payload["access_token"]

    def fetch_job_offers(
        self,
        range_value: str = "0-49",
        query_params: dict | None = None,
    ) -> list[RawOffer]:
        access_token = self.fetch_access_token()

        params = {
            "range": range_value,
        }

        if query_params:
            params.update(query_params)

        response = httpx.get(
            f"{self.api_url}/v2/offres/search",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params=params,
            timeout=self.timeout,
        )

        if response.status_code == 204:
            return []

        response.raise_for_status()

        payload = response.json()

        offers = payload.get("resultats", [])

        return [
            self._map_offer_to_raw_offer(offer)
            for offer in offers
        ]

    def _map_offer_to_raw_offer(
        self,
        offer: dict,
    ) -> RawOffer:
        offer_id = offer.get("id")

        entreprise = offer.get("entreprise") or {}
        lieu_travail = offer.get("lieuTravail") or {}
        salaire = offer.get("salaire") or {}

        return RawOffer(
            source_name=self.SOURCE_NAME,
            source_job_id=offer_id,
            source_url=self._extract_source_url(offer),
            title=offer.get("intitule") or "UNKNOWN",
            company=entreprise.get("nom"),
            raw_description=offer.get("description") or "",
            city=lieu_travail.get("libelle"),
            region=None,
            country="France",
            contract_type_raw=offer.get("typeContrat"),
            work_mode_raw=None,
            salary_raw=salaire.get("libelle"),
            published_at_raw=offer.get("dateCreation"),
            language_raw="FR",
            retrieved_at=datetime.utcnow(),
            raw_payload=offer,
        )

    @staticmethod
    def _extract_source_url(
        offer: dict,
    ) -> str | None:
        origine_offre = offer.get("origineOffre") or {}
        contact = offer.get("contact") or {}

        if origine_offre.get("urlOrigine"):
            return origine_offre["urlOrigine"]

        if contact.get("urlPostulation"):
            return contact["urlPostulation"]

        return None