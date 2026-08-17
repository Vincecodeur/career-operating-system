from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.applications.models import Application
from app.applications.event_models import ApplicationEvent

from app.applications.schemas import ApplicationCreate
from app.applications.schemas import ApplicationUpdate
from app.applications.schemas import ApplicationResponse
from app.applications.schemas import ApplicationStatusTransition

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

@router.post(
    "",
    response_model=ApplicationResponse
)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    new_application = Application(
    profile_id=application.profile_id,
    job_offer_id=application.job_offer_id,
    status=application.status,
    notes=application.notes,
    source_type=application.source_type
    )

    db.add(new_application)

    db.commit()

    db.refresh(new_application)

    return new_application


@router.get(
    "",
    response_model=list[ApplicationResponse]
)
def list_applications(
    db: Session = Depends(get_db)
):
    return db.query(Application).all()


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

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
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    application.status = application_update.status
    application.notes = application_update.notes
    application.source_type = application_update.source_type

    db.commit()
    db.refresh(application)

    return application


@router.post(
    "/{application_id}/status",
    response_model=ApplicationResponse
)
def transition_application_status(
    application_id: int,
    transition: ApplicationStatusTransition,
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

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