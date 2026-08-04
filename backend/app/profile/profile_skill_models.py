from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class ProfileSkill(Base):
    __tablename__ = "profile_skills"

    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        primary_key=True
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    self_assessment_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Intermediate"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )