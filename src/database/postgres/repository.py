from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging.mixin import LoggedMixin
from src.database.postgres.model import BaseModel


class BaseRepository[T: BaseModel](LoggedMixin):
    """Generic async repository providing common CRUD operations backed by SQLAlchemy."""

    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an active AsyncSession."""
        self.session = session

    async def create(self, instance: T) -> T:
        """Add a new entity instance to the database session, flush, and refresh it.

        :param instance: The model instance to persist.
        :return: The created model instance with updated DB defaults/IDs.
        """
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)

        self.logger.debug(
            "Created entity",
            model=self.model.__name__,
            id=getattr(instance, "id", None),
        )
        return instance

    async def get_by_id(self, id_: UUID | str | int) -> T | None:
        """Fetch a single entity instance by its primary key.

        :param id_: The primary key identifier.
        :return: The model instance if found, otherwise None.
        """
        return await self.session.get(self.model, id_)

    async def get_all(self) -> Sequence[T]:
        """Fetch all entity records for this repository's model.

        :return: A sequence of all model instances in the table.
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, instance: T) -> T:
        """Flush pending changes on an existing entity and refresh its attributes.

        :param instance: The updated model instance.
        :return: The refreshed model instance.
        """
        merged_instance = await self.session.merge(instance)
        await self.session.flush()

        self.logger.debug(
            "Updated entity",
            model=self.model.__name__,
            id=getattr(instance, "id", None),
        )
        return merged_instance

    async def delete(self, instance: T) -> None:
        """Mark an entity instance for deletion and flush the session.

        :param instance: The model instance to delete.
        """
        entity_id = getattr(instance, "id", None)
        await self.session.delete(instance)
        await self.session.flush()

        self.logger.debug(
            "Deleted entity",
            model=self.model.__name__,
            id=entity_id,
        )
