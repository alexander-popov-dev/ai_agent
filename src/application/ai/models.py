from uuid import UUID

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy import UUID as SAUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.postgres.model import BaseModel


class AIProvider(BaseModel):
    __tablename__ = "ai_provider"

    name: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    models: Mapped[list["AIModel"]] = relationship(
        back_populates="provider",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AIModel(BaseModel):
    __tablename__ = "ai_model"

    name: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    provider_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey(column="ai_provider.id", ondelete="CASCADE"),
        index=True,
    )
    provider: Mapped["AIProvider"] = relationship(back_populates="models")
