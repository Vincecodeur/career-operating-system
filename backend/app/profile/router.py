from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.profile.models import Profile
from app.profile.schemas import ProfileCreate
from app.profile.schemas import ProfileResponse

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)


@router.post(
    "",
    response_model=ProfileResponse
)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):
    new_profile = Profile(
        profile_name=profile.profile_name,
        full_name=profile.full_name,
        current_title=profile.current_title,
        location=profile.location,
        years_of_experience=profile.years_of_experience,
        target_role_short_term=profile.target_role_short_term,
        target_role_long_term=profile.target_role_long_term,
        remote_preference=profile.remote_preference,
        preferred_countries=profile.preferred_countries
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get(
    "",
    response_model=list[ProfileResponse]
)
def list_profiles(
    db: Session = Depends(get_db)
):
    return db.query(Profile).all()


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Profile).filter(
        Profile.id == profile_id
    ).first()