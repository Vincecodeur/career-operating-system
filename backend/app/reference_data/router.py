from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.reference_data.models import ContractType
from app.reference_data.models import Country
from app.reference_data.models import WorkMode
from app.reference_data.schemas import ContractTypeResponse
from app.reference_data.schemas import CountryResponse
from app.reference_data.schemas import WorkModeResponse

router = APIRouter(
    prefix="/reference-data",
    tags=["Reference Data"],
)


@router.get(
    "/countries",
    response_model=list[CountryResponse],
)
def list_countries(
    db: Session = Depends(get_db),
):
    return (
        db.query(Country)
        .order_by(Country.name)
        .all()
    )


@router.get(
    "/work-modes",
    response_model=list[WorkModeResponse],
)
def list_work_modes(
    db: Session = Depends(get_db),
):
    return (
        db.query(WorkMode)
        .order_by(WorkMode.name)
        .all()
    )


@router.get(
    "/contract-types",
    response_model=list[ContractTypeResponse],
)
def list_contract_types(
    db: Session = Depends(get_db),
):
    return (
        db.query(ContractType)
        .order_by(ContractType.name)
        .all()
    )