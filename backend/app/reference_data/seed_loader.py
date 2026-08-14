import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.reference_data.models import ContractType
from app.reference_data.models import Country
from app.reference_data.models import WorkMode


SEEDS_DIR = Path(__file__).parent / "seeds"


def _load_json(filename: str) -> list:
    with open(
        SEEDS_DIR / filename,
        encoding="utf-8"
    ) as file:
        return json.load(file)


def seed_countries(db: Session) -> None:
    countries = _load_json("countries.json")

    for country in countries:
        exists = (
            db.query(Country)
            .filter(
                Country.code == country["code"]
            )
            .first()
        )

        if not exists:
            db.add(
                Country(
                    code=country["code"],
                    name=country["name"],
                )
            )

    db.commit()


def seed_work_modes(db: Session) -> None:
    work_modes = _load_json(
        "work_modes.json"
    )

    for work_mode in work_modes:
        exists = (
            db.query(WorkMode)
            .filter(
                WorkMode.code == work_mode["code"]
            )
            .first()
        )

        if not exists:
            db.add(
                WorkMode(
                    code=work_mode["code"],
                    name=work_mode["name"],
                )
            )

    db.commit()


def seed_contract_types(
    db: Session,
) -> None:
    contract_types = _load_json(
        "contract_types.json"
    )

    for contract_type in contract_types:
        exists = (
            db.query(ContractType)
            .filter(
                ContractType.code
                == contract_type["code"]
            )
            .first()
        )

        if not exists:
            db.add(
                ContractType(
                    code=contract_type["code"],
                    name=contract_type["name"],
                )
            )

    db.commit()


def seed_reference_data(
    db: Session,
) -> None:
    seed_countries(db)
    seed_work_modes(db)
    seed_contract_types(db)