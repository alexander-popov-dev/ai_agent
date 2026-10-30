from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from src.application.niche.models import Niche
from src.database.postgres.repository import BaseRepository


class NicheRepository(BaseRepository[Niche]):
    """Repository for managing Niche entity database operations."""

    model = Niche

    async def get_all_by_user(self, user_id: UUID | str) -> Sequence[Niche]:
        """Fetch all niches belonging to a specific user.

        :param user_id: Identifier of the owner user.
        :return: Sequence of Niche entities.
        """

        statement = select(self.model).where(self.model.user_id == user_id and self.model.is_active.is_active(True))
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
