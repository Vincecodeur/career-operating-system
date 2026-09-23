from datetime import datetime

from pydantic import BaseModel


class JobOfferCreate(BaseModel):
    title: str
    company_name: str | None = None
    location: str | None = None
    source: str | None = None
    source_url: str | None = None
    description: str


class JobOfferResponse(BaseModel):
    id: int
    title: str
    company_name: str | None = None
    location: str | None = None
    source: str | None = None
    source_url: str | None = None
    description: str
    quality_level: str
    seniority: str | None = None
    work_mode: str | None = None
    created_at: datetime

    # DEC-093 - non stocké en base, renseigné uniquement par
    # complete_job_offer_description() pour indiquer au frontend si
    # l'extraction de métadonnées a réussi, afin d'afficher un
    # message invitant à relancer en cas d'échec (Gemini
    # indisponible).
    metadata_extraction_status: str | None = None

    model_config = {
        "from_attributes": True,
    }

class JobOfferDescriptionUpdate(BaseModel):
    description: str
