from typing import Annotated

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dishka import Provider, provide, Scope, FromComponent
from redis.asyncio import Redis

from src.core.logging.mixin import LoggedMixin
from src.telegram.settings import get_telegram_settings, TelegramSettings


class TelegramProvider(Provider, LoggedMixin):

    @provide(scope=Scope.APP)
    def get_settings(self) -> TelegramSettings:
        return get_telegram_settings()

    @provide(scope=Scope.APP)
    async def get_bot(self, settings: TelegramSettings) -> Bot:
        return Bot(
            token=settings.telegram_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            )
        )

    @provide(scope=Scope.APP)
    async def get_redis_storage(self, client: Annotated[Redis, FromComponent("fsm")]) -> RedisStorage:
        return RedisStorage(redis=client)

    @provide(scope=Scope.APP)
    async def get_dispatcher(self, storage: RedisStorage) -> Dispatcher:
        return Dispatcher(storage=storage)
