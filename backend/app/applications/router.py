from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.applications.models import Application
from app.applications.schemas import ApplicationCreate
from app.applications.schemas import ApplicationUpdate
from app.applications.schemas import ApplicationResponse
from app.core.database import get_db


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


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