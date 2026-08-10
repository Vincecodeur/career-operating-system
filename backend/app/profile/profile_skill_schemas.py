from datetime import datetime

from pydantic import BaseModel


class ProfileSkillCreate(BaseModel):
    profile_id: int
    skill_id: int
    years_of_experience: int
    self_assessment_level: str


class ProfileSkillUpdate(BaseModel):
    years_of_experience: int
    self_assessment_level: str


class ProfileSkillResponse(BaseModel):
    profile_id: int
    skill_id: int
    years_of_experience: int
    self_assessment_level: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }