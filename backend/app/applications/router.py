from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.applications.models import Application
from app.applications.event_models import ApplicationEvent
from app.jobs.models import JobOffer
from app.profile.models import Profile

from app.applications.schemas import ApplicationCreate
from app.applications.schemas import ApplicationUpdate
from app.applications.schemas import ApplicationResponse
from app.applications.schemas import ApplicationStatusTransition
from app.applications.schemas import ApplicationEventResponse

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

VALID_TRANSITIONS = {
    "Applied": [
        "Phone Screen",
        "Rejected",
        "Withdrawn"
    ],
    "Phone Screen": [
        "Interview",
        "Rejected",
        "Withdrawn"
    ],
    "Interview": [
        "Offer",
        "Rejected",
        "Withdrawn"
    ],
    "Offer": [
        "Accepted",
        "Rejected",
        "Withdrawn"
    ],
    "Accepted": [],
    "Rejected": [],
    "Withdrawn": []
}

def get_profile_or_404(
    db: Session,
    profile_id: int,
    current_user: User,
) -> Profile:
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
        Profile.user_id == current_user.id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    if not profile.is_active:
        raise HTTPException(
            status_code=400,
            detail="The selected profile is not available."
        )

    return profile


def get_job_offer_or_404(
    db: Session,
    job_offer_id: int,
) -> JobOffer:
    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found."
        )

    return job_offer

@router.post(
    "",
    response_model=ApplicationResponse
)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = get_profile_or_404(
        db=db,
        profile_id=application.profile_id,
        current_user=current_user,
    )

    job_offer = get_job_offer_or_404(
        db=db,
        job_offer_id=application.job_offer_id,
    )

    new_application = Application(
        profile_id=profile.id,
        job_offer_id=job_offer.id,
        status=application.status,
        notes=application.notes,
        source_type=application.source_type,
    )

    db.add(new_application)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(new_application)

    return new_application


@router.get(
    "",
    response_model=list[ApplicationResponse]
)
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Application)
        .join(Profile)
        .filter(Profile.user_id == current_user.id)
        .all()
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .join(Profile)
        .filter(
            Application.id == application_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    return application


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse
)
def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .join(Profile)
        .filter(
            Application.id == application_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    profile = get_profile_or_404(
        db=db,
        profile_id=application_update.profile_id,
        current_user=current_user,
    )

    old_profile_id = application.profile_id
    new_profile_id = profile.id

    application.profile_id = new_profile_id
    application.status = application_update.status
    application.notes = application_update.notes
    application.source_type = application_update.source_type

    if old_profile_id != new_profile_id:
        profile_changed_event = ApplicationEvent(
            application_id=application.id,
            event_type="PROFILE_CHANGED",
            old_value=str(old_profile_id),
            new_value=str(new_profile_id),
        )

        db.add(profile_changed_event)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(application)

    return application


@router.post(
    "/{application_id}/status",
    response_model=ApplicationResponse
)
def transition_application_status(
    application_id: int,
    transition: ApplicationStatusTransition,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .join(Profile)
        .filter(
            Application.id == application_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    current_status = application.status
    new_status = transition.status

    if new_status not in VALID_TRANSITIONS.get(
        current_status,
        []
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition."
        )

    application.status = new_status

    event = ApplicationEvent(
        application_id=application.id,
        event_type="STATUS_CHANGED",
        old_value=current_status,
        new_value=new_status
    )

    db.add(event)

    db.commit()

    db.refresh(application)

    return application

@router.get(
    "/{application_id}/timeline",
    response_model=list[ApplicationEventResponse]
)
def get_application_timeline(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .join(Profile)
        .filter(
            Application.id == application_id,
            Profile.user_id == current_user.id,
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    return (
        db.query(ApplicationEvent)
        .filter(
            ApplicationEvent.application_id == application_id
        )
        .order_by(
            ApplicationEvent.event_date.desc()
        )
        .all()
    )
