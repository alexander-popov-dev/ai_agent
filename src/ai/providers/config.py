from pydantic import BaseModel

from src.ai.providers.enum import Provider
from src.paths import BASE_DIR

PROVIDERS_PATH = BASE_DIR / "src" / "ai" / "providers" / "providers.yaml"


class ProviderConfig(BaseModel):
    provider: Provider
    base_url: str | None = None
    api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key


class ProvidersConfig(BaseModel):
    providers: dict[Provider, ProviderConfig]
