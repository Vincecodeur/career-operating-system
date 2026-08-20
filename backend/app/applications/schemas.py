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
    profile_id: int
    status: str
    notes: str | None = None
    source_type: str = "MANUAL"
    
class ApplicationStatusTransition(BaseModel):
    status: str

class ApplicationResponse(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
        
class ApplicationEventResponse(BaseModel):
    id: int
    application_id: int
    event_type: str
    old_value: str | None = None
    new_value: str | None = None
    event_date: datetime

    class Config:
        from_attributes = True