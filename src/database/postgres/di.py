from typing import AsyncIterator

from dishka import Provider, provide, Scope
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection
from psycopg.rows import DictRow, dict_row
from psycopg_pool import AsyncConnectionPool
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging.mixin import LoggedMixin
from src.database.postgres.engine import DatabaseEngine, settings


class PostgresProvider(Provider, LoggedMixin):

    @provide(scope=Scope.APP)
    async def get_database(self) -> AsyncIterator[DatabaseEngine]:
        db = DatabaseEngine()
        yield db
        await db.close()

    @provide(scope=Scope.REQUEST)
    async def get_session(self, db: DatabaseEngine) -> AsyncIterator[AsyncSession]:
        async with db.session_factory() as session:
            try:
                self.logger.info("Session established")
                yield session
                await session.commit()
                self.logger.info("Session commited")
            except Exception:
                await session.rollback()
                self.logger.info("Session rollback")
                raise

    @provide(scope=Scope.APP)
    async def get_checkpointer(self) -> AsyncIterator[AsyncPostgresSaver]:
        raw_dsn: str = settings.url.replace("+asyncpg", "")
        pool = AsyncConnectionPool[AsyncConnection[DictRow]](
            conninfo=raw_dsn,
            max_size=20,
            open=False,
            kwargs={"row_factory": dict_row},
        )
        await pool.open()

        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()

        yield checkpointer
        await pool.close()
