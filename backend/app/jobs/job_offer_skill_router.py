from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.job_offer_skill_schemas import (
    JobOfferSkillCreate,
    JobOfferSkillResponse,
)
from app.jobs.models import JobOffer
from app.skills.models import Skill

router = APIRouter(
    tags=["Job Offer Skills"]
)


@router.post(
    "/job-offer-skills",
    response_model=JobOfferSkillResponse
)
def create_job_offer_skill(
    job_offer_skill: JobOfferSkillCreate,
    db: Session = Depends(get_db)
):
    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_skill.job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found."
        )

    skill = db.query(Skill).filter(
        Skill.id == job_offer_skill.skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found."
        )

    relation = JobOfferSkill(
        job_offer_id=job_offer_skill.job_offer_id,
        skill_id=job_offer_skill.skill_id,
        is_required=job_offer_skill.is_required
    )

    db.add(relation)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This skill is already linked to this job offer."
        )

    db.refresh(relation)

    return relation


@router.get(
    "/job-offer-skills",
    response_model=list[JobOfferSkillResponse]
)
def list_job_offer_skills(
    db: Session = Depends(get_db)
):
    return db.query(JobOfferSkill).all()


@router.get(
    "/job-offers/{job_offer_id}/skills",
    response_model=list[JobOfferSkillResponse]
)
def list_skills_for_job_offer(
    job_offer_id: int,
    db: Session = Depends(get_db)
):
    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found."
        )

    return db.query(JobOfferSkill).filter(
        JobOfferSkill.job_offer_id == job_offer_id
    ).all()