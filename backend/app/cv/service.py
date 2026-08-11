from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.cv.models import CV


CV_STORAGE_ROOT = Path("storage") / "cvs"


def save_cv_file(
    profile_id: int,
    uploaded_file: UploadFile,
) -> tuple[str, str, int, str]:
    original_file_name = Path(uploaded_file.filename or "cv").name
    file_suffix = Path(original_file_name).suffix

    stored_file_name = f"{uuid4()}{file_suffix}"

    profile_storage_path = CV_STORAGE_ROOT / f"profile_{profile_id}"
    profile_storage_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination_path = profile_storage_path / stored_file_name

    with destination_path.open("wb") as destination_file:
        copyfileobj(
            uploaded_file.file,
            destination_file,
        )

    file_size_bytes = destination_path.stat().st_size
    mime_type = uploaded_file.content_type or "application/octet-stream"

    return (
        stored_file_name,
        original_file_name,
        file_size_bytes,
        mime_type,
    )


def clear_default_cv_for_profile(
    profile_id: int,
    db: Session,
) -> None:
    existing_default_cvs = db.query(CV).filter(
        CV.profile_id == profile_id,
        CV.is_default.is_(True),
    ).all()

    for existing_cv in existing_default_cvs:
        existing_cv.is_default = False


def delete_cv_file(
    storage_path: str,
) -> None:
    path = Path(storage_path)

    if path.exists() and path.is_file():
        path.unlink()