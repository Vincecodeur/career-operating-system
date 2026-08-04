from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class JobOfferSkill(Base):
    __tablename__ = "job_offer_skills"

    job_offer_id: Mapped[int] = mapped_column(
        ForeignKey("job_offers.id"),
        primary_key=True
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )