from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.postgres.model import BaseModel

if TYPE_CHECKING:
    from src.application.niche.models import Niche
    from src.application.pipeline.models import UserPipelineSettings

class User(BaseModel):
    __tablename__ = "user"

    external_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    user_pipeline_settings: Mapped[list["UserPipelineSettings"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    niches: Mapped[list["Niche"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
