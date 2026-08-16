from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.profile.models import Profile
from app.profile.profile_soft_skill_models import ProfileSoftSkill
from app.profile.profile_soft_skill_schemas import ProfileSoftSkillCreate
from app.profile.profile_soft_skill_schemas import ProfileSoftSkillResponse


router = APIRouter(
    tags=["Profile Soft Skills"],
)


@router.get(
    "/profiles/{profile_id}/soft-skills",
    response_model=list[ProfileSoftSkillResponse],
)
def list_soft_skills_for_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    return db.query(ProfileSoftSkill).filter(
        ProfileSoftSkill.profile_id == profile_id
    ).order_by(
        ProfileSoftSkill.name
    ).all()


@router.post(
    "/profile-soft-skills",
    response_model=ProfileSoftSkillResponse,
)
def create_profile_soft_skill(
    soft_skill: ProfileSoftSkillCreate,
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(
        Profile.id == soft_skill.profile_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    normalized_name = soft_skill.name.strip()

    if not normalized_name:
        raise HTTPException(
            status_code=400,
            detail="Soft skill name is required.",
        )

    new_soft_skill = ProfileSoftSkill(
        profile_id=soft_skill.profile_id,
        name=normalized_name,
    )

    db.add(new_soft_skill)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This soft skill already exists for this profile.",
        )

    db.refresh(new_soft_skill)

    return new_soft_skill


@router.delete(
    "/profile-soft-skills/{soft_skill_id}",
)
def delete_profile_soft_skill(
    soft_skill_id: int,
    db: Session = Depends(get_db),
):
    soft_skill = db.query(ProfileSoftSkill).filter(
        ProfileSoftSkill.id == soft_skill_id
    ).first()

    if soft_skill is None:
        raise HTTPException(
            status_code=404,
            detail="Soft skill not found.",
        )

    db.delete(soft_skill)
    db.commit()

    return {
        "message": "Soft skill deleted successfully."
    }