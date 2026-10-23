from functools import cache

from pydantic import SecretStr, Field

from src.settings import BaseProjectSettings


class AIProjectSettings(BaseProjectSettings):
    google_api_key: SecretStr | None = Field(
        default=None,
        alias="GOOGLE_API_KEY",
    )
    openrouter_api_key: SecretStr | None = Field(
        default=None,
        alias="OPENROUTER_API_KEY",
    )

    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        alias="OPENROUTER_BASE_URL",
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )


@cache
def get_ai_project_settings() -> AIProjectSettings:
    return AIProjectSettings()


