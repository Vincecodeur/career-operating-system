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