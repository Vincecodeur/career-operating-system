from datetime import date
from datetime import datetime

from pydantic import BaseModel


class WorkExperienceCreate(BaseModel):
    profile_id: int
    company_name: str
    job_title: str
    start_date: date
    end_date: date | None = None
    is_current_position: bool = False
    description: str


class WorkExperienceUpdate(BaseModel):
    company_name: str
    job_title: str
    start_date: date
    end_date: date | None = None
    is_current_position: bool = False
    description: str


class WorkExperienceResponse(BaseModel):
    id: int
    profile_id: int
    company_name: str
    job_title: str
    start_date: date
    end_date: date | None
    is_current_position: bool
    description: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }