from functools import cache

from pydantic import Field

from src.settings import BaseProjectSettings


class TelegramSettings(BaseProjectSettings):
    telegram_token: str = Field(alias="TELEGRAM_BOT_TOKEN")


@cache
def get_telegram_settings() -> TelegramSettings:
    return TelegramSettings()