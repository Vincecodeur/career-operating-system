from datetime import datetime

import httpx

from app.core.settings import settings
from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.raw_offer_schema import RawOffer


class GreenhouseConnector(ConnectorInterface):
    """
    Connecteur Greenhouse pour le pipeline Job Discovery.

    Cette implementation utilise l'API publique Greenhouse Job Board.

    L'objectif MVP est volontairement simple :
    - un board token configure ;
    - recuperation des offres publiees ;
    - mapping vers RawOffer ;
    - integration au ConnectorRegistry.

    Le connecteur ne realise aucune normalisation,
    aucune persistance, aucun matching et aucun scoring.
    """

    SOURCE_NAME = "Greenhouse"

    def __init__(
        self,
        board_token: str | None = None,
        api_url: str | None = None,
        timeout: int | None = None,
    ):
        self.board_token = (
            board_token
            or settings.GREENHOUSE_BOARD_TOKEN
        )
        self.api_url = (
            api_url
            or settings.GREENHOUSE_API_URL
        )
        self.timeout = (
            timeout
            or settings.GREENHOUSE_TIMEOUT
        )

    def fetch_job_offers(
        self,
        query_params: dict | None = None,
    ) -> list[RawOffer]:
        if not self.board_token:
            return []

        if not self.api_url:
            return []

        try:
            response = httpx.get(
                self._build_jobs_url(),
                params=query_params or {},
                timeout=self.timeout,
            )

            if response.status_code == 204:
                return []

            response.raise_for_status()

            payload = response.json()

            jobs = self._extract_jobs(
                payload
            )

            return [
                self._map_job_to_raw_offer(
                    job
                )
                for job in jobs
            ]

        except httpx.HTTPError:
            return []

    def _build_jobs_url(
        self,
    ) -> str:
        return (
            f"{self.api_url.rstrip('/')}/"
            f"{self.board_token}/jobs"
        )

    def _extract_jobs(
        self,
        payload,
    ) -> list[dict]:
        if not isinstance(
            payload,
            dict,
        ):
            return []

        jobs = payload.get(
            "jobs"
        )

        if not isinstance(
            jobs,
            list,
        ):
            return []

        return [
            job
            for job in jobs
            if isinstance(
                job,
                dict,
            )
        ]

    def _map_job_to_raw_offer(
        self,
        job: dict,
    ) -> RawOffer:
        location = self._extract_location(
            job
        )

        return RawOffer(
            source_name=self.SOURCE_NAME,
            source_job_id=self._extract_job_id(
                job
            ),
            source_url=self._extract_source_url(
                job
            ),
            title=self._extract_title(
                job
            ),
            company=self._extract_company(
                job
            ),
            raw_description=self._extract_description(
                job
            ),
            city=location["city"],
            region=location["region"],
            country=location["country"],
            contract_type_raw=self._extract_contract_type(
                job
            ),
            work_mode_raw=None,
            salary_raw=None,
            published_at_raw=self._extract_published_at(
                job
            ),
            language_raw=self._extract_language(
                job
            ),
            retrieved_at=datetime.utcnow(),
            raw_payload=job,
        )

    @staticmethod
    def _extract_job_id(
        job: dict,
    ) -> str | None:
        job_id = job.get(
            "id"
        )

        if job_id is None:
            return None

        return str(
            job_id
        )

    @staticmethod
    def _extract_source_url(
        job: dict,
    ) -> str | None:
        return job.get(
            "absolute_url"
        )

    @staticmethod
    def _extract_title(
        job: dict,
    ) -> str:
        title = job.get(
            "title"
        )

        if not title:
            return "UNKNOWN"

        return str(
            title
        )

    @staticmethod
    def _extract_company(
        job: dict,
    ) -> str | None:
        company_name = job.get(
            "company_name"
        )

        if company_name:
            return str(
                company_name
            )

        return None

    @staticmethod
    def _extract_description(
        job: dict,
    ) -> str:
        content = job.get(
            "content"
        )

        if content:
            return str(
                content
            )

        description = job.get(
            "description"
        )

        if description:
            return str(
                description
            )

        return ""

    @staticmethod
    def _extract_location(
        job: dict,
    ) -> dict:
        location = job.get(
            "location"
        )

        if isinstance(
            location,
            dict,
        ):
            return {
                "city": location.get(
                    "name"
                ),
                "region": None,
                "country": None,
            }

        if isinstance(
            location,
            str,
        ):
            return {
                "city": location,
                "region": None,
                "country": None,
            }

        return {
            "city": None,
            "region": None,
            "country": None,
        }

    @staticmethod
    def _extract_contract_type(
        job: dict,
    ) -> str | None:
        metadata = job.get(
            "metadata"
        )

        if not isinstance(
            metadata,
            list,
        ):
            return None

        for item in metadata:
            if not isinstance(
                item,
                dict,
            ):
                continue

            name = item.get(
                "name"
            )

            if name == "Job Family":
                value = item.get(
                    "value"
                )

                if value:
                    return str(
                        value
                    )

        return None

    @staticmethod
    def _extract_published_at(
        job: dict,
    ) -> str | None:
        published_at = job.get(
            "first_published"
        )

        if published_at:
            return str(
                published_at
            )

        updated_at = job.get(
            "updated_at"
        )

        if updated_at:
            return str(
                updated_at
            )

        return None

    @staticmethod
    def _extract_language(
        job: dict,
    ) -> str | None:
        language = job.get(
            "language"
        )

        if language:
            return str(
                language
            )

        return None