from pydantic import BaseModel


class MatchingResult(BaseModel):
    profile_id: int
    job_offer_id: int
    matching_score: float

    matching_skills: list[str]
    missing_skills: list[str]