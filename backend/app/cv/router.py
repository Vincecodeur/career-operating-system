from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.cv.models import CV
from app.cv.parsing_schemas import ParsedCVResponse
from app.cv.parsing_service import CVParsingError
from app.cv.parsing_service import parse_cv_file
from app.cv.schemas import CVResponse
from app.cv.schemas import CVUpdate
from app.cv.service import clear_default_cv_for_profile
from app.cv.service import delete_cv_file
from app.cv.service import save_cv_file
from app.profile.models import Profile


router = APIRouter(
    tags=["CVs"],
)


@router.post(
    "/profiles/{profile_id}/cvs",
    response_model=CVResponse,
)
def create_cv(
    profile_id: int,
    cv_file: UploadFile = File(...),
    language: str | None = Form(None),
    version_label: str | None = Form(None),
    is_default: bool = Form(False),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    (
        file_name,
        original_file_name,
        file_size_bytes,
        mime_type,
    ) = save_cv_file(
        profile_id,
        cv_file,
    )

    storage_path = str(
        Path("storage")
        / "cvs"
        / f"profile_{profile_id}"
        / file_name
    )

    if is_default:
        clear_default_cv_for_profile(
            profile_id,
            db,
        )

    new_cv = CV(
        profile_id=profile_id,
        file_name=file_name,
        original_file_name=original_file_name,
        storage_path=storage_path,
        file_size_bytes=file_size_bytes,
        mime_type=mime_type,
        language=language,
        version_label=version_label,
        is_default=is_default,
        parsing_status="PENDING",
    )

    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)

    return new_cv


@router.get(
    "/profiles/{profile_id}/cvs",
    response_model=list[CVResponse],
)
def list_cvs_for_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    return db.query(CV).filter(
        CV.profile_id == profile_id,
    ).all()


@router.get(
    "/cvs/{cv_id}",
    response_model=CVResponse,
)
def get_cv(
    cv_id: int,
    db: Session = Depends(get_db),
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    return cv


@router.get(
    "/cvs/{cv_id}/download",
)
def download_cv(
    cv_id: int,
    db: Session = Depends(get_db),
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    return FileResponse(
        path=cv.storage_path,
        filename=cv.original_file_name,
    )


@router.put(
    "/cvs/{cv_id}",
    response_model=CVResponse,
)
def update_cv(
    cv_id: int,
    cv_update: CVUpdate,
    db: Session = Depends(get_db),
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    cv.language = cv_update.language
    cv.version_label = cv_update.version_label

    db.commit()
    db.refresh(cv)

    return cv


@router.post(
    "/cvs/{cv_id}/set-default",
    response_model=CVResponse,
)
def set_default_cv(
    cv_id: int,
    db: Session = Depends(get_db),
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    clear_default_cv_for_profile(
        cv.profile_id,
        db,
    )

    cv.is_default = True

    db.commit()
    db.refresh(cv)

    return cv


@router.post(
    "/cvs/{cv_id}/parse",
    response_model=ParsedCVResponse,
)
def parse_cv(
    cv_id: int,
    db: Session = Depends(get_db),
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    cv.parsing_status = "PROCESSING"
    db.commit()
    db.refresh(cv)

    try:
        raw_text, parsed_data = parse_cv_file(
            Path(cv.storage_path),
        )
    except CVParsingError as exc:
        cv.parsing_status = "FAILED"
        db.commit()
        db.refresh(cv)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    cv.parsing_status = "COMPLETED"
    db.commit()
    db.refresh(cv)

    return ParsedCVResponse(
        cv_id=cv.id,
        parsing_status=cv.parsing_status,
        raw_text_length=len(raw_text),
        extracted_text_preview=raw_text[:500],
        parsed_data=parsed_data,
    )


@router.delete(
    "/cvs/{cv_id}",
    response_model=CVResponse,
)
def delete_cv(
    cv_id: int,
    db: Session = Depends(get_db),
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    deleted_cv = cv

    db.delete(cv)
    db.commit()

    delete_cv_file(
        deleted_cv.storage_path,
    )

    return deleted_cv