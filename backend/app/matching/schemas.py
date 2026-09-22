from pydantic import BaseModel
from datetime import datetime


class AIExplanationSummary(BaseModel):
    summary: str
    detailed_explanation: str
    action_plan: list[str]
    provider_name: str
    model_name: str
    prompt_version: str
    generated_at: datetime


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

    is_calculable: bool = True

    # 7.2.0.7 - AI Explanation Frontend Implementation : lu depuis
    # job_offer_ai_explanations si une explication existe déjà pour
    # cette paire (profile_id, job_offer_id), jamais généré à la volée
    # (DEC-089 : génération réservée au run quotidien planifié).
    ai_explanation: AIExplanationSummary | None = None


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

    is_calculable: bool = True
    
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
    is_calculable: bool = True