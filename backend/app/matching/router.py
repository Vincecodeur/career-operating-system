from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db
from app.jobs.models import JobOffer
from app.matching.schemas import MatchingResult
from app.matching.schemas import ProfileOpportunityScore
from app.matching.schemas import RankedJobOffer
from app.matching.service import calculate_matching_result
from app.matching.service import calculate_profile_scores_for_job_offer
from app.matching.service import rank_job_offers_for_profile
from app.profile.models import Profile

router = APIRouter(
    tags=["Matching"]
)


@router.get(
    "/matching/{profile_id}/{job_offer_id}",
    response_model=MatchingResult
)
def calculate_match(
    profile_id: int,
    job_offer_id: int,
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

    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found."
        )

    return calculate_matching_result(
        profile_id=profile_id,
        job_offer_id=job_offer_id,
        db=db
    )


@router.get(
    "/profiles/{profile_id}/ranked-job-offers",
    response_model=list[RankedJobOffer]
)
def get_ranked_job_offers(
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

    return rank_job_offers_for_profile(
        profile_id=profile_id,
        db=db
    )

@router.get(
    "/matching/job-offers/{job_offer_id}/profiles",
    response_model=list[ProfileOpportunityScore],
)
def get_profile_scores_for_job_offer(
    job_offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

    if job_offer is None:
        raise HTTPException(
            status_code=404,
            detail="Job offer not found.",
        )

    return calculate_profile_scores_for_job_offer(
        job_offer_id=job_offer_id,
        db=db,
        user_id=current_user.id,
    )
