from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.skills.models import Skill
from app.skills.schemas import SkillCreate
from app.skills.schemas import SkillResponse
from app.skills.schemas import SkillUpdate

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


@router.post(
    "",
    response_model=SkillResponse
)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db)
):
    new_skill = Skill(
        name=skill.name,
        category=skill.category
    )

    db.add(new_skill)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A skill with this name already exists."
        )

    db.refresh(new_skill)

    return new_skill


@router.get(
    "",
    response_model=list[SkillResponse]
)
def list_skills(
    db: Session = Depends(get_db)
):
    return db.query(Skill).all()


@router.get(
    "/{skill_id}",
    response_model=SkillResponse
)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found."
        )

    return skill

@router.put(
    "/{skill_id}",
    response_model=SkillResponse
)
def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found."
        )

    skill.name = skill_update.name
    skill.category = skill_update.category

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A skill with this name already exists."
        )

    db.refresh(skill)

    return skill
