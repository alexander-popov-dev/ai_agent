from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Boolean, Integer, ForeignKey, UniqueConstraint, Float, Text
from sqlalchemy import UUID as SAUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.pipelines.core.enums import PipelineSessionStatus
from src.database.postgres.model import BaseModel

if TYPE_CHECKING:
    from src.application.user.models import User
    from src.application.ai.models import AIModel

class Pipeline(BaseModel):
    __tablename__ = "pipeline"

    name: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    steps: Mapped[list["PipelineStep"]] = relationship(
        back_populates="pipeline",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class PipelineStep(BaseModel):
    __tablename__ = "pipeline_step"

    name: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    agent: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    system_prompt: Mapped[str] = mapped_column(String)
    user_prompt: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    pipeline_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey(column="pipeline.id", ondelete="CASCADE"),
        index=True,
    )
    pipeline: Mapped["Pipeline"] = relationship(back_populates="steps")
    user_settings: Mapped["UserPipelineSettings | None"] = relationship(uselist=False)


class UserPipelineSettings(BaseModel):
    __tablename__ = "user_pipeline_settings"
    __table_args__ = (
        UniqueConstraint("user_id", "step_id", name="uq_user_step"),
    )
    user_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )
    step_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey("pipeline_step.id", ondelete="CASCADE"),
        index=True,
    )
    model_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey("ai_model.id", ondelete="RESTRICT"),
        index=True,
        nullable=True,
    )
    temperature: Mapped[float | int] = mapped_column(
        Float,
        nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="user_pipeline_settings")
    model: Mapped["AIModel"] = relationship()


class UserPipelineSession(BaseModel):
    __tablename__ = "user_pipeline_session"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    pipeline_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey(column="pipeline.id", ondelete="CASCADE"),
        index=True,
    )
    step_id: Mapped[UUID | None] = mapped_column(
        SAUUID,
        ForeignKey(column="pipeline_step.id", ondelete="SET NULL"),
        index=True,
    )
    status: Mapped[PipelineSessionStatus] = mapped_column(
        String(50),
        default=PipelineSessionStatus.CREATED,
        nullable=False
    )
    error_message: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    error_traceback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )