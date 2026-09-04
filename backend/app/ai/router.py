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
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db
from app.profile.models import Profile


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
    current_user: User = Depends(get_current_user),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
        Profile.user_id == current_user.id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

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