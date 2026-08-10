from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.experience.models import WorkExperience
from app.experience.schemas import WorkExperienceCreate
from app.experience.schemas import WorkExperienceUpdate
from app.experience.schemas import WorkExperienceResponse
from app.profile.models import Profile


router = APIRouter(
    tags=["Work Experiences"]
)


@router.post(
    "/work-experiences",
    response_model=WorkExperienceResponse
)
def create_work_experience(
    work_experience: WorkExperienceCreate,
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.id == work_experience.profile_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    new_work_experience = WorkExperience(
        profile_id=work_experience.profile_id,
        company_name=work_experience.company_name,
        job_title=work_experience.job_title,
        start_date=work_experience.start_date,
        end_date=work_experience.end_date,
        is_current_position=work_experience.is_current_position,
        description=work_experience.description
    )

    db.add(new_work_experience)
    db.commit()
    db.refresh(new_work_experience)

    return new_work_experience


@router.get(
    "/work-experiences",
    response_model=list[WorkExperienceResponse]
)
def list_work_experiences(
    db: Session = Depends(get_db)
):
    return db.query(WorkExperience).all()


@router.get(
    "/work-experiences/{work_experience_id}",
    response_model=WorkExperienceResponse
)
def get_work_experience(
    work_experience_id: int,
    db: Session = Depends(get_db)
):
    work_experience = db.query(WorkExperience).filter(
        WorkExperience.id == work_experience_id
    ).first()

    if work_experience is None:
        raise HTTPException(
            status_code=404,
            detail="Work experience not found."
        )

    return work_experience


@router.get(
    "/profiles/{profile_id}/work-experiences",
    response_model=list[WorkExperienceResponse]
)
def list_work_experiences_for_profile(
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

    return db.query(WorkExperience).filter(
        WorkExperience.profile_id == profile_id
    ).all()
    
    
@router.put(
    "/work-experiences/{work_experience_id}",
    response_model=WorkExperienceResponse
)
def update_work_experience(
    work_experience_id: int,
    work_experience_update: WorkExperienceUpdate,
    db: Session = Depends(get_db)
):
    work_experience = db.query(WorkExperience).filter(
        WorkExperience.id == work_experience_id
    ).first()

    if work_experience is None:
        raise HTTPException(
            status_code=404,
            detail="Work experience not found."
        )

    work_experience.company_name = (
        work_experience_update.company_name
    )
    work_experience.job_title = (
        work_experience_update.job_title
    )
    work_experience.start_date = (
        work_experience_update.start_date
    )
    work_experience.end_date = (
        work_experience_update.end_date
    )
    work_experience.is_current_position = (
        work_experience_update.is_current_position
    )
    work_experience.description = (
        work_experience_update.description
    )

    db.commit()
    db.refresh(work_experience)

    return work_experience

@router.delete(
    "/work-experiences/{work_experience_id}"
)
def delete_work_experience(
    work_experience_id: int,
    db: Session = Depends(get_db)
):
    work_experience = db.query(WorkExperience).filter(
        WorkExperience.id == work_experience_id
    ).first()

    if work_experience is None:
        raise HTTPException(
            status_code=404,
            detail="Work experience not found."
        )

    db.delete(work_experience)
    db.commit()

    return {
        "message": "Work experience deleted."
    }