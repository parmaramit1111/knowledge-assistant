from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


class BaseEntity(Base):
    """
    Common entity fields shared across all database models.
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    created_by: Mapped[str] = mapped_column(
        String(200),
        default=None,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_by: Mapped[str] = mapped_column(
        String(200),
        default=None,
        nullable=True,
    )

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )
    deleted_by: Mapped[str] = mapped_column(
        String(200),
        default=None,
        nullable=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )