from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class JobOffer(Base):
    __tablename__ = "job_offers"

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

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    company_name: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    region: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    country: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="UNKNOWN"
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    source_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    url_primary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    description_raw: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    description_normalized: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="UNKNOWN"
    )

    work_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UNKNOWN"
    )

    contract_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UNKNOWN"
    )

    seniority: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UNKNOWN"
    )

    salary_min: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    salary_max: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    salary_currency: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    salary_original_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    skills_extracted: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True
    )

    skills_normalized: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True
    )

    quality_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PARTIAL"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
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


Index(
    "idx_job_offer_deduplication",
    JobOffer.title,
    JobOffer.company_name,
    JobOffer.city
)