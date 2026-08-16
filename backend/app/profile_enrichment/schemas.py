from datetime import datetime

from pydantic import BaseModel


class AcceptProposalRequest(BaseModel):
    proposed_value_override: str | None = None
    reference_id: int | None = None
    
class BulkProposalRequest(BaseModel):
    profile_id: int
    cv_id: int


class BulkProposalResponse(BaseModel):
    processed: int
    
class ProfileEnrichmentProposalResponse(BaseModel):
    id: int
    profile_id: int
    cv_id: int
    proposal_type: str
    status: str
    source_field: str
    target_field: str
    observed_value: str
    normalized_value: str
    current_profile_value: str | None
    proposed_value: str
    reference_id: int | None
    conflict_detected: bool
    rejection_reason: str | None
    created_at: datetime
    validated_at: datetime | None

    model_config = {
        "from_attributes": True
    }
    
