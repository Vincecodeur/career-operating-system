from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base
from app.profile_enrichment.enums import ProfileEnrichmentProposalStatus


class ProfileEnrichmentProposal(Base):
    __tablename__ = "profile_enrichment_proposals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=False,
        index=True,
    )

    cv_id: Mapped[int] = mapped_column(
        ForeignKey("cvs.id"),
        nullable=False,
        index=True,
    )

    proposal_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=ProfileEnrichmentProposalStatus.PENDING.value,
        index=True,
    )

    source_field: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_field: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    observed_value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    normalized_value: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True,
    )

    current_profile_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    proposed_value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    reference_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    conflict_detected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )