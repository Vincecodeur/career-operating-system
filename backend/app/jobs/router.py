from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.jobs.models import JobOffer
from app.jobs.schemas import JobOfferCreate
from app.jobs.schemas import JobOfferResponse

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