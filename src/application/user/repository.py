from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.application.user.models import User
from src.database.postgres.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_external_id(self, external_id: str) -> User | None:
        statement = (
            select(self.model)
            .where(self.model.external_id == external_id)
            .options(selectinload(self.model.niches))
        )
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none()
