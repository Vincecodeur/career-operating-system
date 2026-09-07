from datetime import datetime

from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    discovery_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    discovery_interval_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1440,
    )

    discovery_connectors: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    search_target_job_titles: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    search_preferred_countries: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    search_work_modes: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    search_included_keywords: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    search_excluded_keywords: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    discovery_age_window: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="30_DAYS",
    )

    discovery_minimum_matching_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=25,
    )

    discovery_show_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    discovery_default_sort: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="BEST_MATCH_FIRST",
    )

    ai_features_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    ai_consent_accepted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    linkedin_email_imap_host: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    linkedin_email_imap_port: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    linkedin_email_address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    linkedin_email_app_password_encrypted: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    linkedin_email_folder: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="INBOX",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    keyword: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    application_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sort_by: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
