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
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class JobOfferDescriptionUpdate(BaseModel):
    description: str
