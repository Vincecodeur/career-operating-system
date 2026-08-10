from datetime import datetime

from pydantic import BaseModel


class SkillCreate(BaseModel):
    name: str
    category: str


class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    
class SkillUpdate(BaseModel):
    name: str
    category: str