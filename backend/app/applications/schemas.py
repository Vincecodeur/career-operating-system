from datetime import datetime

from pydantic import BaseModel


class ApplicationBase(BaseModel):
    profile_id: int
    job_offer_id: int
    status: str = "Applied"
    notes: str | None = None
    source_type: str = "MANUAL"


class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: str
    notes: str | None = None
    source_type: str = "MANUAL"

class ApplicationResponse(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True