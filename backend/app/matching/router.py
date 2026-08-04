from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.models import JobOffer
from app.matching.schemas import MatchingResult
from app.profile.profile_skill_models import ProfileSkill
from app.profile.models import Profile
from app.skills.models import Skill

router = APIRouter(
    tags=["Matching"]
)


@router.get(
    "/matching/{profile_id}/{job_offer_id}",
    response_model=MatchingResult
)
def calculate_match(
    profile_id: int,
    job_offer_id: int,
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.id == profile_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found."
        )

    profile_skill_ids = {
        item.skill_id
        for item in db.query(ProfileSkill).filter(
            ProfileSkill.profile_id == profile_id
        ).all()
    }

    job_offer_skill_ids = {
        item.skill_id
        for item in db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == job_offer_id
        ).all()
    }

    matching_ids = (
        profile_skill_ids
        & job_offer_skill_ids
    )

    missing_ids = (
        job_offer_skill_ids
        - profile_skill_ids
    )

    matching_skills = [
        skill.name
        for skill in db.query(Skill).filter(
            Skill.id.in_(matching_ids)
        ).all()
    ]

    missing_skills = [
        skill.name
        for skill in db.query(Skill).filter(
            Skill.id.in_(missing_ids)
        ).all()
    ]

    if len(job_offer_skill_ids) == 0:
        score = 0.0
    else:
        score = round(
            (
                len(matching_ids)
                / len(job_offer_skill_ids)
            ) * 100,
            2
        )

    return MatchingResult(
        profile_id=profile_id,
        job_offer_id=job_offer_id,
        matching_score=score,
        matching_skills=matching_skills,
        missing_skills=missing_skills
    )