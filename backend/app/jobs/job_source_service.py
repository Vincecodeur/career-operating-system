from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.jobs.job_source_models import JobSource


class JobSourceService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_sources(
        self,
    ) -> list[JobSource]:
        return (
            self.db.query(JobSource)
            .order_by(JobSource.name)
            .all()
        )

    def update_source(
        self,
        source_id: int,
        is_active: bool,
    ) -> JobSource:
        source = (
            self.db.query(JobSource)
            .filter(JobSource.id == source_id)
            .first()
        )

        if source is None:
            raise HTTPException(
                status_code=404,
                detail="Job source not found.",
            )

        if not is_active:
            active_sources = (
                self.db.query(JobSource)
                .filter(
                    JobSource.is_active.is_(True)
                )
                .count()
            )

            if (
                active_sources <= 1
                and source.is_active
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "At least one discovery source "
                        "must remain active."
                    ),
                )

        source.is_active = is_active

        self.db.commit()
        self.db.refresh(source)

        return source