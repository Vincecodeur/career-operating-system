from datetime import date
from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    issuing_organization: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class ProfileCertification(Base):
    __tablename__ = "profile_certifications"

    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        primary_key=True
    )

    certification_id: Mapped[int] = mapped_column(
        ForeignKey("certifications.id"),
        primary_key=True
    )

    obtained_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    expiration_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    credential_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )