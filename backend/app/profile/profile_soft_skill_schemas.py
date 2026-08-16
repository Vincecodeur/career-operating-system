from datetime import datetime

from pydantic import BaseModel


class ProfileSoftSkillCreate(BaseModel):
    profile_id: int
    name: str


class ProfileSoftSkillResponse(BaseModel):
    id: int
    profile_id: int
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }