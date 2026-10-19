from dishka import AsyncContainer, make_async_container

from src.application.ai.di import AIProviderProvider
from src.database.redis.di import RedisFSMDBProvider
from src.application.niche.di import NicheProvider
from src.application.pipeline.di import PipelineProvider
from src.application.user.di import UserProvider
from src.database.postgres.di import PostgresProvider
from src.telegram.di import TelegramProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        PostgresProvider(),
        RedisFSMDBProvider(),
        TelegramProvider(),
        AIProviderProvider(),
        UserProvider(),
        NicheProvider(),
        PipelineProvider(),
    )
