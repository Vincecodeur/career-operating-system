from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.certifications.models import Certification
from app.certifications.models import ProfileCertification
from app.certifications.schemas import CertificationCreate
from app.certifications.schemas import CertificationResponse
from app.certifications.schemas import ProfileCertificationCreate
from app.certifications.schemas import ProfileCertificationResponse
from app.certifications.schemas import ProfileCertificationUpdate
from app.core.database import get_db
from app.profile.models import Profile

router = APIRouter(
    tags=["Certifications"]
)


@router.post(
    "/certifications",
    response_model=CertificationResponse
)
def create_certification(
    certification: CertificationCreate,
    db: Session = Depends(get_db)
):
    new_certification = Certification(
        name=certification.name,
        issuing_organization=certification.issuing_organization
    )

    db.add(new_certification)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A certification with this name already exists."
        )

    db.refresh(new_certification)

    return new_certification


@router.get(
    "/certifications",
    response_model=list[CertificationResponse]
)
def list_certifications(
    db: Session = Depends(get_db)
):
    return db.query(Certification).all()


@router.get(
    "/certifications/{certification_id}",
    response_model=CertificationResponse
)
def get_certification(
    certification_id: int,
    db: Session = Depends(get_db)
):
    certification = db.query(Certification).filter(
        Certification.id == certification_id
    ).first()

    if certification is None:
        raise HTTPException(
            status_code=404,
            detail="Certification not found."
        )

    return certification


@router.post(
    "/profile-certifications",
    response_model=ProfileCertificationResponse
)
def create_profile_certification(
    profile_certification: ProfileCertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_certification.profile_id,
        Profile.user_id == current_user.id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    certification = db.query(Certification).filter(
        Certification.id == profile_certification.certification_id
    ).first()

    if certification is None:
        raise HTTPException(
            status_code=404,
            detail="Certification not found."
        )

    new_profile_certification = ProfileCertification(
        profile_id=profile_certification.profile_id,
        certification_id=profile_certification.certification_id,
        obtained_date=profile_certification.obtained_date,
        expiration_date=profile_certification.expiration_date,
        credential_id=profile_certification.credential_id
    )

    db.add(new_profile_certification)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This certification is already linked to this profile."
        )

    db.refresh(new_profile_certification)

    return new_profile_certification


@router.get(
    "/profile-certifications",
    response_model=list[ProfileCertificationResponse]
)
def list_profile_certifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(ProfileCertification)
        .join(Profile)
        .filter(Profile.user_id == current_user.id)
        .all()
    )


@router.get(
    "/profiles/{profile_id}/certifications",
    response_model=list[ProfileCertificationResponse]
)
def list_certifications_for_profile(
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

    return db.query(ProfileCertification).filter(
        ProfileCertification.profile_id == profile_id
    ).all()
    
    
@router.put(
    "/profile-certifications/{profile_id}/{certification_id}",
    response_model=ProfileCertificationResponse,
)
def update_profile_certification(
    profile_id: int,
    certification_id: int,
    profile_certification_update: ProfileCertificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_certification = (
        db.query(ProfileCertification)
        .join(Profile)
        .filter(
            ProfileCertification.profile_id == profile_id,
            ProfileCertification.certification_id == certification_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if profile_certification is None:
        raise HTTPException(
            status_code=404,
            detail="Profile certification not found.",
        )

    profile_certification.obtained_date = (
        profile_certification_update.obtained_date
    )
    profile_certification.expiration_date = (
        profile_certification_update.expiration_date
    )
    profile_certification.credential_id = (
        profile_certification_update.credential_id
    )

    db.commit()
    db.refresh(profile_certification)

    return profile_certification

@router.delete(
    "/profile-certifications/{profile_id}/{certification_id}",
)
def delete_profile_certification(
    profile_id: int,
    certification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_certification = (
        db.query(ProfileCertification)
        .join(Profile)
        .filter(
            ProfileCertification.profile_id == profile_id,
            ProfileCertification.certification_id == certification_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if profile_certification is None:
        raise HTTPException(
            status_code=404,
            detail="Profile certification not found.",
        )

    db.delete(profile_certification)

    db.commit()

    return {
        "message": "Profile certification deleted successfully."
    }
