from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db
from app.settings.schemas import AISettingsResponse
from app.settings.schemas import AISettingsUpdate
from app.settings.schemas import (
    DiscoveryPreferencesSettingsResponse,
)
from app.settings.schemas import (
    DiscoveryPreferencesSettingsUpdate,
)
from app.settings.schemas import (
    JobDiscoverySettingsResponse,
)
from app.settings.schemas import (
    JobDiscoverySettingsUpdate,
)
from app.settings.schemas import SavedSearch
from app.settings.schemas import SavedSearchCreate
from app.settings.schemas import (
    SearchCriteriaSettingsResponse,
)
from app.settings.schemas import (
    SearchCriteriaSettingsUpdate,
)
from app.settings.service import SettingsService


router = APIRouter(
    tags=["settings"],
)


@router.get(
    "/settings/job-discovery",
    response_model=JobDiscoverySettingsResponse,
)
def get_job_discovery_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    return service.get_job_discovery_settings(
        current_user.id
    )


@router.put(
    "/settings/job-discovery",
    response_model=JobDiscoverySettingsResponse,
)
def update_job_discovery_settings(
    payload: JobDiscoverySettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    service.update_job_discovery_settings(
        current_user.id,
        payload.model_dump(),
    )

    return service.get_job_discovery_settings(
        current_user.id
    )


@router.get(
    "/settings/search-criteria",
    response_model=SearchCriteriaSettingsResponse,
)
def get_search_criteria_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    return service.get_search_criteria_settings(
        current_user.id
    )


@router.put(
    "/settings/search-criteria",
    response_model=SearchCriteriaSettingsResponse,
)
def update_search_criteria_settings(
    payload: SearchCriteriaSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    service.update_search_criteria_settings(
        current_user.id,
        payload.model_dump(),
    )

    return service.get_search_criteria_settings(
        current_user.id
    )


@router.get(
    "/settings/discovery-preferences",
    response_model=DiscoveryPreferencesSettingsResponse,
)
def get_discovery_preferences_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    return (
        service.get_discovery_preferences_settings(
            current_user.id
        )
    )


@router.put(
    "/settings/discovery-preferences",
    response_model=DiscoveryPreferencesSettingsResponse,
)
def update_discovery_preferences_settings(
    payload: DiscoveryPreferencesSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    service.update_discovery_preferences_settings(
        current_user.id,
        payload.model_dump(),
    )

    return (
        service.get_discovery_preferences_settings(
            current_user.id
        )
    )


@router.get(
    "/settings/ai",
    response_model=AISettingsResponse,
)
def get_ai_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    return service.get_ai_settings(
        current_user.id
    )


@router.put(
    "/settings/ai",
    response_model=AISettingsResponse,
)
def update_ai_settings(
    payload: AISettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    try:
        service.update_ai_settings(
            current_user.id,
            payload.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return service.get_ai_settings(
        current_user.id
    )


@router.get(
    "/settings/saved-searches",
    response_model=list[SavedSearch],
)
def get_saved_searches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    return service.get_saved_searches(
        current_user.id
    )


@router.post(
    "/settings/saved-searches",
    response_model=SavedSearch,
)
def create_saved_search(
    payload: SavedSearchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    return service.create_saved_search(
        current_user.id,
        payload.model_dump(),
    )


@router.delete(
    "/settings/saved-searches/{saved_search_id}",
    response_model=SavedSearch,
)
def delete_saved_search(
    saved_search_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = SettingsService(db)

    try:
        return service.delete_saved_search(
            current_user.id,
            saved_search_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail="Saved search not found.",
        ) from exc
