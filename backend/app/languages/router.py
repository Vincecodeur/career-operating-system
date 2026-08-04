from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.languages.schemas import LanguageCreate
from app.languages.schemas import LanguageResponse
from app.languages.schemas import ProfileLanguageCreate
from app.languages.schemas import ProfileLanguageResponse
from app.profile.models import Profile

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
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.id == profile_language.profile_id
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
    db: Session = Depends(get_db)
):
    return db.query(ProfileLanguage).all()


@router.get(
    "/profiles/{profile_id}/languages",
    response_model=list[ProfileLanguageResponse]
)
def list_languages_for_profile(
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

    return db.query(ProfileLanguage).filter(
        ProfileLanguage.profile_id == profile_id
    ).all()