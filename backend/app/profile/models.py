from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Text

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    profile_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    current_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    target_role_short_term: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    target_role_long_term: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    remote_preference: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    preferred_countries: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    
    professional_summary: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
    )

    career_motivations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    preferred_environment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    non_negotiables: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    additional_context: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    cvs = relationship(
    "CV",
    back_populates="profile",
    cascade="all, delete-orphan",
    )