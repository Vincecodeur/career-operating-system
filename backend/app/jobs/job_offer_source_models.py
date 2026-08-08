from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class JobOfferSource(Base):
    __tablename__ = "job_offer_sources"

    __table_args__ = (
        UniqueConstraint(
            "job_offer_id",
            "job_source_id",
            "source_url",
            name="uq_job_offer_source_url"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    uuid: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
        index=True
    )

    job_offer_id: Mapped[int] = mapped_column(
        ForeignKey("job_offers.id"),
        nullable=False,
        index=True
    )

    job_source_id: Mapped[int] = mapped_column(
        ForeignKey("job_sources.id"),
        nullable=False,
        index=True
    )

    source_job_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
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