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
    professional_summary: str | None = None
    career_motivations: str | None = None
    preferred_environment: str | None = None
    non_negotiables: str | None = None
    additional_context: str | None = None


class ProfileUpdate(BaseModel):
    profile_name: str
    full_name: str
    current_title: str
    location: str
    years_of_experience: int
    target_role_short_term: str
    target_role_long_term: str
    remote_preference: str
    preferred_countries: str
    professional_summary: str | None = None
    career_motivations: str | None = None
    preferred_environment: str | None = None
    non_negotiables: str | None = None
    additional_context: str | None = None


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
    professional_summary: str | None = None
    career_motivations: str | None = None
    preferred_environment: str | None = None
    non_negotiables: str | None = None
    additional_context: str | None = None

    model_config = {
        "from_attributes": True
    }
    
