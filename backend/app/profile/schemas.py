from datetime import datetime

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    profile_name: str
    full_name: str
    current_title: str
    location: str
    years_of_experience: int
    target_role_short_term: str
    target_role_long_term: str
    remote_preference: str
    preferred_countries: str


class ProfileResponse(BaseModel):
    id: int
    profile_name: str
    full_name: str
    current_title: str
    location: str
    years_of_experience: int
    target_role_short_term: str
    target_role_long_term: str
    remote_preference: str
    preferred_countries: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }