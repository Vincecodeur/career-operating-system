from datetime import datetime

from pydantic import BaseModel


class CVCreate(BaseModel):
    profile_id: int
    file_name: str
    original_file_name: str
    storage_path: str
    file_size_bytes: int
    mime_type: str
    language: str | None = None
    version_label: str | None = None
    is_default: bool = False
    parsing_status: str = "PENDING"


class CVUpdate(BaseModel):
    language: str | None = None
    version_label: str | None = None


class CVResponse(BaseModel):
    id: int
    profile_id: int
    file_name: str
    original_file_name: str
    storage_path: str
    file_size_bytes: int
    mime_type: str
    language: str | None
    version_label: str | None
    is_default: bool
    parsing_status: str
    uploaded_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }