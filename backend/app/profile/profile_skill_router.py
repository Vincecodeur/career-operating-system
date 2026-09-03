from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.profile.profile_skill_schemas import ProfileSkillCreate
from app.profile.profile_skill_schemas import ProfileSkillResponse
from app.profile.profile_skill_schemas import ProfileSkillUpdate
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_skill.profile_id,
        Profile.user_id == current_user.id,
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(ProfileSkill)
        .join(Profile)
        .filter(Profile.user_id == current_user.id)
        .all()
    )


@router.get(
    "/profiles/{profile_id}/skills",
    response_model=list[ProfileSkillResponse]
)
def list_skills_for_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
        Profile.user_id == current_user.id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    return db.query(ProfileSkill).filter(
        ProfileSkill.profile_id == profile_id
    ).all()


@router.put(
    "/profile-skills/{profile_id}/{skill_id}",
    response_model=ProfileSkillResponse
)
def update_profile_skill(
    profile_id: int,
    skill_id: int,
    profile_skill_update: ProfileSkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_skill = (
        db.query(ProfileSkill)
        .join(Profile)
        .filter(
            ProfileSkill.profile_id == profile_id,
            ProfileSkill.skill_id == skill_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if profile_skill is None:
        raise HTTPException(
            status_code=404,
            detail="Profile skill relationship not found."
        )

    profile_skill.years_of_experience = (
        profile_skill_update.years_of_experience
    )
    profile_skill.self_assessment_level = (
        profile_skill_update.self_assessment_level
    )

    db.commit()
    db.refresh(profile_skill)

    return profile_skill


@router.delete(
    "/profile-skills/{profile_id}/{skill_id}",
    response_model=ProfileSkillResponse
)
def delete_profile_skill(
    profile_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_skill = (
        db.query(ProfileSkill)
        .join(Profile)
        .filter(
            ProfileSkill.profile_id == profile_id,
            ProfileSkill.skill_id == skill_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if profile_skill is None:
        raise HTTPException(
            status_code=404,
            detail="Profile skill relationship not found."
        )

    deleted_profile_skill = {
        "profile_id": profile_skill.profile_id,
        "skill_id": profile_skill.skill_id,
        "years_of_experience": profile_skill.years_of_experience,
        "self_assessment_level": profile_skill.self_assessment_level,
        "created_at": profile_skill.created_at,
    }

    db.delete(profile_skill)
    db.commit()

    return deleted_profile_skill