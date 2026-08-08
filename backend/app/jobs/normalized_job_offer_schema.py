from pydantic import BaseModel
from pydantic import ConfigDict


class NormalizedJobOffer(BaseModel):
    """
    Représente une offre normalisée prête à être
    persistée ou comparée avec un profil candidat.
    """

    title: str

    company: str | None = None

    description_raw: str

    description_normalized: str | None = None

    url_primary: str

    language: str

    city: str | None = None

    region: str | None = None

    country: str

    work_mode: str

    contract_type: str

    seniority: str

    salary_min: int | None = None

    salary_max: int | None = None

    salary_currency: str | None = None

    salary_original_text: str | None = None

    skills_extracted: list[str] = []

    skills_normalized: list[str] = []

    quality_level: str

    status: str = "ACTIVE"

    model_config = ConfigDict(
        extra="forbid"
    )