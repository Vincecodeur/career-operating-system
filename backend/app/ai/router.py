from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.ai.context_schemas import (
    AIContextPreviewResponse,
)
from app.ai.context_service import (
    AIContextService,
)
from app.core.database import get_db


router = APIRouter(
    tags=["ai-context"],
)


@router.get(
    "/profiles/{profile_id}/ai-context-preview",
    response_model=AIContextPreviewResponse,
)
def get_ai_context_preview(
    profile_id: int,
    db: Session = Depends(get_db),
):
    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile_id
    )

    if preview is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    return preview