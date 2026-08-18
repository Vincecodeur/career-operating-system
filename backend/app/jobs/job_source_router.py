from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.jobs.job_source_schemas import (
    JobSourceResponse,
    JobSourceUpdate,
)

from app.jobs.job_source_service import (
    JobSourceService,
)

router = APIRouter(
    tags=["Job Sources"]
)


@router.get(
    "/job-sources",
    response_model=list[JobSourceResponse]
)
def get_job_sources(
    db: Session = Depends(get_db)
):
    return JobSourceService(
        db
    ).get_sources()


@router.put(
    "/job-sources/{source_id}",
    response_model=JobSourceResponse
)
def update_job_source(
    source_id: int,
    payload: JobSourceUpdate,
    db: Session = Depends(get_db)
):
    return JobSourceService(
        db
    ).update_source(
        source_id=source_id,
        is_active=payload.is_active,
    )