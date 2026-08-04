from datetime import datetime

from pydantic import BaseModel


class LanguageCreate(BaseModel):
    name: str


class LanguageResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProfileLanguageCreate(BaseModel):
    profile_id: int
    language_id: int
    proficiency_level: str


class ProfileLanguageResponse(BaseModel):
    profile_id: int
    language_id: int
    proficiency_level: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }