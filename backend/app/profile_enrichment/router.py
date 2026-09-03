from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db
from app.profile_enrichment.schemas import (
    AcceptProposalRequest,
    BulkProposalRequest,
    BulkProposalResponse,
    ProfileEnrichmentProposalResponse,
)
from app.profile_enrichment.service import accept_proposal
from app.profile_enrichment.service import generate_proposals_for_cv
from app.profile_enrichment.service import list_proposals_for_profile
from app.profile_enrichment.service import reject_proposal
from app.profile_enrichment.service import accept_all_proposals
from app.profile_enrichment.service import reject_all_proposals


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
    current_user: User = Depends(get_current_user),
):
    return generate_proposals_for_cv(
        cv_id,
        db,
        current_user,
    )


@router.get(
    "/profiles/{profile_id}/enrichment",
    response_model=list[ProfileEnrichmentProposalResponse],
)
def get_profile_enrichment_proposals(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_proposals_for_profile(
        profile_id,
        db,
        current_user,
    )


@router.post(
    "/enrichment/{proposal_id}/accept",
    response_model=ProfileEnrichmentProposalResponse,
)
def accept_profile_enrichment_proposal(
    proposal_id: int,
    payload: AcceptProposalRequest | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    proposed_value_override = (
        payload.proposed_value_override
        if payload is not None
        else None
    )

    reference_id = (
        payload.reference_id
        if payload is not None
        else None
    )

    return accept_proposal(
        proposal_id=proposal_id,
        proposed_value_override=proposed_value_override,
        reference_id=reference_id,
        db=db,
        current_user=current_user,
    )


@router.post(
    "/enrichment/{proposal_id}/reject",
    response_model=ProfileEnrichmentProposalResponse,
)
def reject_profile_enrichment_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return reject_proposal(
        proposal_id,
        db,
        current_user,
    )
    
@router.post(
    "/enrichment/accept-all",
    response_model=BulkProposalResponse,
)
def accept_all_profile_enrichment_proposals(
    payload: BulkProposalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    processed = accept_all_proposals(
        profile_id=payload.profile_id,
        cv_id=payload.cv_id,
        db=db,
        current_user=current_user,
    )

    return {
        "processed": processed,
    }

@router.post(
    "/enrichment/reject-all",
    response_model=BulkProposalResponse,
)
def reject_all_profile_enrichment_proposals(
    payload: BulkProposalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    processed = reject_all_proposals(
        profile_id=payload.profile_id,
        cv_id=payload.cv_id,
        db=db,
        current_user=current_user,
    )

    return {
        "processed": processed,
    }