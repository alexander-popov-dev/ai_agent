import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, UUID as SAUUID, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """SQLAlchemy declarative agents: UUID primary key, auto-managed created_at and updated_at."""

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(SAUUID, primary_key=True, default=uuid.uuid4)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
