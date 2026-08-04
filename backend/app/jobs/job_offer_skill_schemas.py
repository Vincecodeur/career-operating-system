from datetime import datetime

from pydantic import BaseModel


class JobOfferSkillCreate(BaseModel):
    job_offer_id: int
    skill_id: int
    is_required: bool = True


class JobOfferSkillResponse(BaseModel):
    job_offer_id: int
    skill_id: int
    is_required: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }