from datetime import date
from datetime import datetime

from pydantic import BaseModel


class CertificationCreate(BaseModel):
    name: str
    issuing_organization: str


class CertificationResponse(BaseModel):
    id: int
    name: str
    issuing_organization: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProfileCertificationCreate(BaseModel):
    profile_id: int
    certification_id: int
    obtained_date: date | None = None
    expiration_date: date | None = None
    credential_id: str | None = None


class ProfileCertificationResponse(BaseModel):
    profile_id: int
    certification_id: int
    obtained_date: date | None
    expiration_date: date | None
    credential_id: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }