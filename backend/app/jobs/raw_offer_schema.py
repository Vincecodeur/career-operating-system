from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class RawOffer(BaseModel):
    """
    Représente une offre brute récupérée depuis une source externe
    avant toute normalisation.
    """

    source_name: str

    source_job_id: str | None = None

    source_url: str | None = None

    title: str

    company: str | None = None

    raw_description: str

    city: str | None = None

    region: str | None = None

    country: str | None = None

    contract_type_raw: str | None = None

    work_mode_raw: str | None = None

    salary_raw: str | None = None

    published_at_raw: str | None = None

    language_raw: str | None = None

    retrieved_at: datetime

    raw_payload: dict | None = None

    model_config = ConfigDict(
        extra="forbid"
    )