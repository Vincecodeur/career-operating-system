from pydantic import BaseModel


class MatchingResult(BaseModel):
    profile_id: int
    job_offer_id: int

    matching_score: float

    skills_score: float
    experience_score: float
    work_mode_score: float
    location_score: float

    matching_skills: list[str]
    missing_skills: list[str]

    strengths: list[str]
    weaknesses: list[str]
    explanations: list[ScoreExplanation]
    opportunity_analysis: OpportunityAnalysis


class RankedJobOffer(BaseModel):
    job_offer_id: int
    title: str

    matching_score: float

    skills_score: float
    experience_score: float
    work_mode_score: float
    location_score: float

    matching_skills: list[str]
    missing_skills: list[str]
    
class ScoreExplanation(BaseModel):
    criterion: str
    score: float
    message: str
    
class OpportunityAnalysis(BaseModel):
    verdict: str
    recommendation: str
    summary: str
    
    

class ProfileOpportunityScore(BaseModel):
    profile_id: int
    profile_name: str

    matching_score: float

    skills_score: float
    experience_score: float
    work_mode_score: float
    location_score: float

    is_best_match: bool