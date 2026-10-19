from typing import TYPE_CHECKING

from sqlalchemy import String, UUID, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID as SAUUID

from src.database.postgres.model import BaseModel

if TYPE_CHECKING:
    from src.application.user.models import User


class Niche(BaseModel):
    __tablename__ = "niche"
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="uq_niche_user"),
    )

    name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[UUID] = mapped_column(
        SAUUID,
        ForeignKey(column="user.id", ondelete="CASCADE"),
        index=True,
    )
    user: Mapped["User"] = relationship(back_populates="niches")
