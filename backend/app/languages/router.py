from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.languages.schemas import LanguageCreate
from app.languages.schemas import LanguageResponse
from app.languages.schemas import ProfileLanguageCreate
from app.languages.schemas import ProfileLanguageResponse
from app.profile.models import Profile
from app.languages.schemas import ProfileLanguageUpdate

router = APIRouter(
    tags=["Languages"]
)


@router.post(
    "/languages",
    response_model=LanguageResponse
)
def create_language(
    language: LanguageCreate,
    db: Session = Depends(get_db)
):
    new_language = Language(
        name=language.name
    )

    db.add(new_language)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A language with this name already exists."
        )

    db.refresh(new_language)

    return new_language


@router.get(
    "/languages",
    response_model=list[LanguageResponse]
)
def list_languages(
    db: Session = Depends(get_db)
):
    return db.query(Language).all()


@router.get(
    "/languages/{language_id}",
    response_model=LanguageResponse
)
def get_language(
    language_id: int,
    db: Session = Depends(get_db)
):
    language = db.query(Language).filter(
        Language.id == language_id
    ).first()

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Language not found."
        )

    return language


@router.post(
    "/profile-languages",
    response_model=ProfileLanguageResponse
)
def create_profile_language(
    profile_language: ProfileLanguageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_language.profile_id,
        Profile.user_id == current_user.id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    language = db.query(Language).filter(
        Language.id == profile_language.language_id
    ).first()

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Language not found."
        )

    new_profile_language = ProfileLanguage(
        profile_id=profile_language.profile_id,
        language_id=profile_language.language_id,
        proficiency_level=profile_language.proficiency_level
    )

    db.add(new_profile_language)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This language is already linked to this profile."
        )

    db.refresh(new_profile_language)

    return new_profile_language


@router.get(
    "/profile-languages",
    response_model=list[ProfileLanguageResponse]
)
def list_profile_languages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(ProfileLanguage)
        .join(Profile)
        .filter(Profile.user_id == current_user.id)
        .all()
    )


@router.get(
    "/profiles/{profile_id}/languages",
    response_model=list[ProfileLanguageResponse]
)
def list_languages_for_profile(
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

    return db.query(ProfileLanguage).filter(
        ProfileLanguage.profile_id == profile_id
    ).all()
    
    
@router.put(
    "/profile-languages/{profile_id}/{language_id}",
    response_model=ProfileLanguageResponse,
)
def update_profile_language(
    profile_id: int,
    language_id: int,
    profile_language_update: ProfileLanguageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_language = (
        db.query(ProfileLanguage)
        .join(Profile)
        .filter(
            ProfileLanguage.profile_id == profile_id,
            ProfileLanguage.language_id == language_id,
            Profile.user_id == current_user.id,
        )
    ).first() 

    if profile_language is None:
        raise HTTPException(
            status_code=404,
            detail="Profile language not found.",
        )

    profile_language.proficiency_level = (
        profile_language_update.proficiency_level
    )

    db.commit()
    db.refresh(profile_language)

    return profile_language


@router.delete(
    "/profile-languages/{profile_id}/{language_id}",
)
def delete_profile_language(
    profile_id: int,
    language_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_language = (
        db.query(ProfileLanguage)
        .join(Profile)
        .filter(
            ProfileLanguage.profile_id == profile_id,
            ProfileLanguage.language_id == language_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if profile_language is None:
        raise HTTPException(
            status_code=404,
            detail="Profile language not found.",
        )

    db.delete(profile_language)
    db.commit()

    return {
        "message": "Profile language deleted successfully."
    }