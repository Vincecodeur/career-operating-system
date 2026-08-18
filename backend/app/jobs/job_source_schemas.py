from pydantic import BaseModel


class JobSourceResponse(BaseModel):
    id: int
    name: str
    source_type: str
    is_active: bool

    model_config = {
        "from_attributes": True,
    }


class JobSourceUpdate(BaseModel):
    is_active: bool