from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.profile_enrichment.schemas import (
    ProfileEnrichmentProposalResponse,
)
from app.profile_enrichment.service import accept_proposal
from app.profile_enrichment.service import generate_proposals_for_cv
from app.profile_enrichment.service import list_proposals_for_profile
from app.profile_enrichment.service import reject_proposal


router = APIRouter(
    tags=["Profile Enrichment"],
)


@router.post(
    "/cvs/{cv_id}/enrichment/generate",
    response_model=list[ProfileEnrichmentProposalResponse],
)
def generate_cv_enrichment_proposals(
    cv_id: int,
    db: Session = Depends(get_db),
):
    return generate_proposals_for_cv(
        cv_id,
        db,
    )


@router.get(
    "/profiles/{profile_id}/enrichment",
    response_model=list[ProfileEnrichmentProposalResponse],
)
def get_profile_enrichment_proposals(
    profile_id: int,
    db: Session = Depends(get_db),
):
    return list_proposals_for_profile(
        profile_id,
        db,
    )


@router.post(
    "/enrichment/{proposal_id}/accept",
    response_model=ProfileEnrichmentProposalResponse,
)
def accept_profile_enrichment_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
):
    return accept_proposal(
        proposal_id,
        db,
    )


@router.post(
    "/enrichment/{proposal_id}/reject",
    response_model=ProfileEnrichmentProposalResponse,
)
def reject_profile_enrichment_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
):
    return reject_proposal(
        proposal_id,
        db,
    )