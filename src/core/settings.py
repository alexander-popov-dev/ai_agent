from functools import cache

from pydantic import Field

from src.settings import BaseProjectSettings


class CoreSettings(BaseProjectSettings):
    debug: bool = Field(alias="DEBUG")
    log_level: str = Field(alias="LOG_LEVEL")
    log_json: bool = Field(alias="LOG_JSON")


@cache
def get_core_settings():
    return CoreSettings()
