from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.jobs.models import JobOffer
from app.jobs.schemas import JobOfferCreate
from app.jobs.schemas import JobOfferDescriptionUpdate
from app.jobs.schemas import JobOfferResponse

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.jobs.job_offer_cleanup_service import delete_stale_job_offers
from app.jobs.job_offer_cleanup_service import resolve_age_window_days
from app.jobs.job_offer_metadata_extraction_service import (
    JobOfferMetadataExtractionService,
)
from app.settings.service import SettingsService
import logging

logger = logging.getLogger(__name__)

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


@router.patch(
    "/job-offers/{job_offer_id}/complete-description",
    response_model=JobOfferResponse,
)
def complete_job_offer_description(
    job_offer_id: int,
    payload: JobOfferDescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Allows manual completion of a PARTIAL-quality job offer's
    description (e.g. LinkedIn Email offers, DEC-086/JOBS-001), by
    pasting the real description copied from the offer's source
    page. Sets quality_level to COMPLETE, unblocking matching score
    calculation for this offer (see
    calculate_matching_result() in app/matching/service.py).
    """
    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found.",
        )

    job_offer.description = payload.description
    job_offer.description_raw = payload.description
    job_offer.quality_level = "COMPLETE"

    db.commit()
    db.refresh(job_offer)

    # DEC-093 - extraction de métadonnées (compétences/séniorité/
    # mode de travail) via Gemini, synchrone mais non bloquante :
    # tout échec (ex. surcharge Gemini 503) n'empêche jamais la
    # sauvegarde de la description elle-même, déjà commitée
    # ci-dessus.
    metadata_extraction_status = "success"

    try:
        JobOfferMetadataExtractionService.extract_and_persist(
            db=db,
            job_offer_id=job_offer.id,
        )
        db.refresh(job_offer)
    except Exception:
        logger.exception(
            "Job offer metadata extraction failed for "
            "job_offer_id=%s.",
            job_offer.id,
        )
        metadata_extraction_status = "failed"

    response = JobOfferResponse.model_validate(job_offer)
    response.metadata_extraction_status = (
        metadata_extraction_status
    )

    return response
