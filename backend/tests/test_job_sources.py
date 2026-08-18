from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import func

from app.core.database import SessionLocal
from app.jobs.job_source_models import JobSource
from app.main import app


client = TestClient(app)


def create_job_source(
    db,
    name: str,
    source_type: str = "API",
    is_active: bool = True,
) -> JobSource:
    job_source = JobSource(
        name=name,
        source_type=source_type,
        is_active=is_active,
    )

    db.add(job_source)
    db.commit()
    db.refresh(job_source)

    return job_source


def cleanup_job_sources(
    db,
    source_names: list[str],
):
    db.query(JobSource).filter(
        JobSource.name.in_(source_names)
    ).delete()

    db.commit()


def test_get_job_sources_returns_sources():
    db = SessionLocal()
    suffix = str(uuid4())
    source_name = f"Test Job Source {suffix}"

    try:
        create_job_source(
            db=db,
            name=source_name,
            source_type="API",
            is_active=True,
        )

        response = client.get("/job-sources")

        assert response.status_code == 200

        data = response.json()

        assert isinstance(
            data,
            list,
        )

        matching_sources = [
            source
            for source in data
            if source["name"] == source_name
        ]

        assert len(matching_sources) == 1
        assert matching_sources[0]["source_type"] == "API"
        assert matching_sources[0]["is_active"] is True

    finally:
        db.rollback()
        cleanup_job_sources(
            db=db,
            source_names=[
                source_name,
            ],
        )
        db.close()


def test_update_job_source_can_disable_source_when_another_active_source_exists():
    db = SessionLocal()
    suffix = str(uuid4())

    source_to_disable_name = f"Source To Disable {suffix}"
    other_active_source_name = f"Other Active Source {suffix}"

    try:
        source_to_disable = create_job_source(
            db=db,
            name=source_to_disable_name,
            source_type="API",
            is_active=True,
        )

        create_job_source(
            db=db,
            name=other_active_source_name,
            source_type="API",
            is_active=True,
        )

        response = client.put(
            f"/job-sources/{source_to_disable.id}",
            json={
                "is_active": False,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == source_to_disable.id
        assert data["is_active"] is False

        db.refresh(source_to_disable)

        assert source_to_disable.is_active is False

    finally:
        db.rollback()
        cleanup_job_sources(
            db=db,
            source_names=[
                source_to_disable_name,
                other_active_source_name,
            ],
        )
        db.close()


def test_update_job_source_can_enable_source():
    db = SessionLocal()
    suffix = str(uuid4())
    source_name = f"Inactive Source {suffix}"

    try:
        source = create_job_source(
            db=db,
            name=source_name,
            source_type="API",
            is_active=False,
        )

        response = client.put(
            f"/job-sources/{source.id}",
            json={
                "is_active": True,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == source.id
        assert data["is_active"] is True

        db.refresh(source)

        assert source.is_active is True

    finally:
        db.rollback()
        cleanup_job_sources(
            db=db,
            source_names=[
                source_name,
            ],
        )
        db.close()


def test_update_job_source_returns_404_for_unknown_source():
    db = SessionLocal()

    try:
        max_source_id = (
            db.query(
                func.max(JobSource.id)
            ).scalar()
            or 0
        )

        unknown_source_id = max_source_id + 9999

        response = client.put(
            f"/job-sources/{unknown_source_id}",
            json={
                "is_active": False,
            },
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Job source not found.",
        }

    finally:
        db.rollback()
        db.close()


def test_update_job_source_cannot_disable_last_active_source():
    db = SessionLocal()
    suffix = str(uuid4())

    source_name = (
        f"Only Active Source {suffix}"
    )

    existing_source_states = {}

    try:
        existing_sources = (
            db.query(JobSource)
            .all()
        )

        existing_source_states = {
            source.id: source.is_active
            for source in existing_sources
        }

        for source in existing_sources:
            source.is_active = False

        db.commit()

        source = create_job_source(
            db=db,
            name=source_name,
            source_type="API",
            is_active=True,
        )

        response = client.put(
            f"/job-sources/{source.id}",
            json={
                "is_active": False,
            },
        )

        assert response.status_code == 400

        assert response.json() == {
            "detail": (
                "At least one discovery source "
                "must remain active."
            ),
        }

        db.refresh(source)

        assert source.is_active is True

    finally:
        db.rollback()

        for (
            source_id,
            is_active,
        ) in existing_source_states.items():
            existing_source = (
                db.query(JobSource)
                .filter(
                    JobSource.id
                    == source_id
                )
                .first()
            )

            if existing_source is not None:
                existing_source.is_active = (
                    is_active
                )

        cleanup_job_sources(
            db=db,
            source_names=[
                source_name,
            ],
        )

        db.commit()
        db.close()