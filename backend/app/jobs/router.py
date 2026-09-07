from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.jobs.models import JobOffer
from app.jobs.schemas import JobOfferCreate
from app.jobs.schemas import JobOfferResponse

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.jobs.job_offer_cleanup_service import delete_stale_job_offers
from app.jobs.job_offer_cleanup_service import resolve_age_window_days
from app.settings.service import SettingsService

router = APIRouter(
    tags=["Job Offers"]
)


@router.post(
    "/job-offers",
    response_model=JobOfferResponse
)
def create_job_offer(
    job_offer: JobOfferCreate,
    db: Session = Depends(get_db)
):
    new_job_offer = JobOffer(
        title=job_offer.title,
        company_name=job_offer.company_name,
        location=job_offer.location,
        source=job_offer.source,
        source_url=job_offer.source_url,
        description=job_offer.description
    )

    db.add(new_job_offer)
    db.commit()
    db.refresh(new_job_offer)

    return new_job_offer


@router.get(
    "/job-offers",
    response_model=list[JobOfferResponse]
)
def list_job_offers(
    db: Session = Depends(get_db)
):
    return db.query(JobOffer).all()


@router.get(
    "/job-offers/{job_offer_id}",
    response_model=JobOfferResponse
)
def get_job_offer(
    job_offer_id: int,
    db: Session = Depends(get_db)
):
    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found."
        )

    return job_offer

@router.post("/job-offers/cleanup")
def cleanup_stale_job_offers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings_service = SettingsService(db)
    discovery_preferences = settings_service.get_discovery_preferences_settings(
        current_user.id
    )

    age_window_days = resolve_age_window_days(
        discovery_preferences["discovery_age_window"]
    )

    return delete_stale_job_offers(db, age_window_days)