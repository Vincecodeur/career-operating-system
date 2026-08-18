from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.settings.schemas import (
    JobDiscoverySettingsResponse,
)
from app.settings.schemas import (
    JobDiscoverySettingsUpdate,
)
from app.settings.service import (
    SettingsService,
)
from app.settings.schemas import (
    SearchCriteriaSettingsResponse,
)

from app.settings.schemas import (
    SearchCriteriaSettingsUpdate,
)



router = APIRouter(
    tags=["settings"],
)


@router.get(
    "/settings/job-discovery",
    response_model=JobDiscoverySettingsResponse,
)
def get_job_discovery_settings(
    db: Session = Depends(get_db),
):
    service = SettingsService(db)

    return service.get_job_discovery_settings()


@router.put(
    "/settings/job-discovery",
    response_model=JobDiscoverySettingsResponse,
)
def update_job_discovery_settings(
    payload: JobDiscoverySettingsUpdate,
    db: Session = Depends(get_db),
):
    service = SettingsService(db)

    service.update_job_discovery_settings(
        payload.model_dump()
    )

    return service.get_job_discovery_settings()


@router.get(
    "/settings/search-criteria",
    response_model=SearchCriteriaSettingsResponse,
)
def get_search_criteria_settings(
    db: Session = Depends(get_db),
):
    service = SettingsService(db)

    return (
        service.get_search_criteria_settings()
    )


@router.put(
    "/settings/search-criteria",
    response_model=SearchCriteriaSettingsResponse,
)
def update_search_criteria_settings(
    payload: SearchCriteriaSettingsUpdate,
    db: Session = Depends(get_db),
):
    service = SettingsService(db)

    service.update_search_criteria_settings(
        payload.model_dump()
    )

    return (
        service.get_search_criteria_settings()
    )