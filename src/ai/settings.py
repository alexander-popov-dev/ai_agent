from functools import cache

from pydantic import SecretStr, Field

from src.settings import BaseProjectSettings


class AIProjectSettings(BaseProjectSettings):
    openrouter_api_key: SecretStr = Field(alias="OPENROUTER_API_KEY")
    google_api_key: SecretStr = Field(alias="GOOGLE_API_KEY")


@cache
def get_ai_project_settings() -> AIProjectSettings:
    return AIProjectSettings()


