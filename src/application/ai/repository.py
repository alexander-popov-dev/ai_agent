from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.application.ai.models import AIModel, AIProvider
from src.database.postgres.repository import BaseRepository


class AIProviderRepository(BaseRepository[AIProvider]):
    model = AIProvider

    async def get_providers_with_models(self) -> Sequence[AIProvider]:
        statement = (
            select(self.model)
            .where(self.model.is_active.is_(True))
            .options(selectinload(self.model.models))
        )
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

class AIModelRepository(BaseRepository[AIModel]):
    model = AIModel
