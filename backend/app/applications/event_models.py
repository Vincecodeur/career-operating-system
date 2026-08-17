from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False
    )

    application = relationship(
        "Application",
        back_populates="events"
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    old_value: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    new_value: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    event_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )