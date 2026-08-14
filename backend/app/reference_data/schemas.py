from datetime import datetime

from pydantic import BaseModel


class CountryResponse(BaseModel):
    id: int
    code: str
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class WorkModeResponse(BaseModel):
    id: int
    code: str
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ContractTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
