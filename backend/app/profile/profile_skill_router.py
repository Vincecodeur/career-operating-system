from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.profile.profile_skill_schemas import ProfileSkillCreate
from app.profile.profile_skill_schemas import ProfileSkillResponse
from app.skills.models import Skill

router = APIRouter(
    tags=["Profile Skills"]
)


@router.post(
    "/profile-skills",
    response_model=ProfileSkillResponse
)
def create_profile_skill(
    profile_skill: ProfileSkillCreate,
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.id == profile_skill.profile_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    skill = db.query(Skill).filter(
        Skill.id == profile_skill.skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found."
        )

    new_profile_skill = ProfileSkill(
        profile_id=profile_skill.profile_id,
        skill_id=profile_skill.skill_id,
        years_of_experience=profile_skill.years_of_experience,
        self_assessment_level=profile_skill.self_assessment_level
    )

    db.add(new_profile_skill)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This skill is already linked to this profile."
        )

    db.refresh(new_profile_skill)

    return new_profile_skill


@router.get(
    "/profile-skills",
    response_model=list[ProfileSkillResponse]
)
def list_profile_skills(
    db: Session = Depends(get_db)
):
    return db.query(ProfileSkill).all()


@router.get(
    "/profiles/{profile_id}/skills",
    response_model=list[ProfileSkillResponse]
)
def list_skills_for_profile(
    profile_id: int,
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

    return db.query(ProfileSkill).filter(
        ProfileSkill.profile_id == profile_id
    ).all()