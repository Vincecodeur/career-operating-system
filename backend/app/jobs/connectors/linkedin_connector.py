from datetime import datetime

import httpx

from app.core.settings import settings
from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.raw_offer_schema import RawOffer


class LinkedInConnector(ConnectorInterface):
    """
    Connecteur LinkedIn pour le pipeline Job Discovery.

    Cette implémentation reste volontairement générique.

    Elle ne suppose pas encore un contrat API LinkedIn définitif.
    Elle permet de valider :
    - l'intégration backend du connecteur ;
    - le mapping vers RawOffer ;
    - l'intégration au ConnectorRegistry ;
    - les tests unitaires.

    Aucun scraping n'est implémenté dans cette phase.
    """

    SOURCE_NAME = "LinkedIn"

    def __init__(
        self,
        api_url: str | None = None,
        access_token: str | None = None,
        timeout: int | None = None,
    ):
        self.api_url = api_url or settings.LINKEDIN_API_URL
        self.access_token = (
            access_token
            or settings.LINKEDIN_ACCESS_TOKEN
        )
        self.timeout = (
            timeout
            or settings.LINKEDIN_TIMEOUT
        )

    def fetch_job_offers(
        self,
        query_params: dict | None = None,
    ) -> list[RawOffer]:
        if not self.api_url:
            return []

        try:
            response = httpx.get(
                self.api_url,
                headers=self._build_headers(),
                params=query_params or {},
                timeout=self.timeout,
            )

            if response.status_code == 204:
                return []

            response.raise_for_status()

            payload = response.json()

            offers = self._extract_offers(
                payload
            )

            return [
                self._map_offer_to_raw_offer(
                    offer
                )
                for offer in offers
            ]

        except httpx.HTTPError:
            return []

    def _build_headers(
        self,
    ) -> dict:
        headers = {
            "Accept": "application/json",
        }

        if self.access_token:
            headers["Authorization"] = (
                f"Bearer {self.access_token}"
            )

        return headers

    def _extract_offers(
        self,
        payload,
    ) -> list[dict]:
        if isinstance(
            payload,
            list,
        ):
            return payload

        if not isinstance(
            payload,
            dict,
        ):
            return []

        possible_keys = [
            "jobs",
            "results",
            "elements",
            "data",
        ]

        for key in possible_keys:
            value = payload.get(
                key
            )

            if isinstance(
                value,
                list,
            ):
                return value

        return []

    def _map_offer_to_raw_offer(
        self,
        offer: dict,
    ) -> RawOffer:
        company = self._extract_company(
            offer
        )

        location = self._extract_location(
            offer
        )

        return RawOffer(
            source_name=self.SOURCE_NAME,
            source_job_id=self._extract_job_id(
                offer
            ),
            source_url=self._extract_source_url(
                offer
            ),
            title=self._extract_title(
                offer
            ),
            company=company,
            raw_description=self._extract_description(
                offer
            ),
            city=location["city"],
            region=location["region"],
            country=location["country"],
            contract_type_raw=self._extract_first_available(
                offer,
                [
                    "contract_type",
                    "employment_type",
                    "contractType",
                ],
            ),
            work_mode_raw=self._extract_first_available(
                offer,
                [
                    "work_mode",
                    "workMode",
                    "remote_policy",
                    "remotePolicy",
                ],
            ),
            salary_raw=self._extract_first_available(
                offer,
                [
                    "salary",
                    "salary_text",
                    "salaryText",
                ],
            ),
            published_at_raw=self._extract_first_available(
                offer,
                [
                    "published_at",
                    "publishedAt",
                    "created_at",
                    "createdAt",
                ],
            ),
            language_raw=self._extract_first_available(
                offer,
                [
                    "language",
                    "language_raw",
                    "languageRaw",
                ],
            ),
            retrieved_at=datetime.utcnow(),
            raw_payload=offer,
        )

    def _extract_job_id(
        self,
        offer: dict,
    ) -> str | None:
        value = self._extract_first_available(
            offer,
            [
                "id",
                "job_id",
                "jobId",
                "urn",
            ],
        )

        if value is None:
            return None

        return str(
            value
        )

    def _extract_title(
        self,
        offer: dict,
    ) -> str:
        value = self._extract_first_available(
            offer,
            [
                "title",
                "job_title",
                "jobTitle",
                "name",
            ],
        )

        if not value:
            return "UNKNOWN"

        return str(
            value
        )

    def _extract_description(
        self,
        offer: dict,
    ) -> str:
        value = self._extract_first_available(
            offer,
            [
                "description",
                "raw_description",
                "summary",
            ],
        )

        if not value:
            return ""

        return str(
            value
        )

    def _extract_company(
        self,
        offer: dict,
    ) -> str | None:
        company = offer.get(
            "company"
        )

        if isinstance(
            company,
            dict,
        ):
            return company.get(
                "name"
            )

        if isinstance(
            company,
            str,
        ):
            return company

        return self._extract_first_available(
            offer,
            [
                "company_name",
                "companyName",
                "organization",
            ],
        )

    def _extract_location(
        self,
        offer: dict,
    ) -> dict:
        location = offer.get(
            "location"
        )

        if isinstance(
            location,
            dict,
        ):
            return {
                "city": location.get(
                    "city"
                ),
                "region": location.get(
                    "region"
                ),
                "country": location.get(
                    "country"
                ),
            }

        if isinstance(
            location,
            str,
        ):
            return {
                "city": location,
                "region": None,
                "country": self._extract_first_available(
                    offer,
                    [
                        "country",
                    ],
                ),
            }

        return {
            "city": self._extract_first_available(
                offer,
                [
                    "city",
                ],
            ),
            "region": self._extract_first_available(
                offer,
                [
                    "region",
                ],
            ),
            "country": self._extract_first_available(
                offer,
                [
                    "country",
                ],
            ),
        }

    def _extract_source_url(
        self,
        offer: dict,
    ) -> str | None:
        return self._extract_first_available(
            offer,
            [
                "source_url",
                "url",
                "apply_url",
                "applyUrl",
                "job_url",
                "jobUrl",
            ],
        )

    @staticmethod
    def _extract_first_available(
        offer: dict,
        keys: list[str],
    ):
        for key in keys:
            value = offer.get(
                key
            )

            if value:
                return value

        return None