from pathlib import Path

from src.ai.config import AIConfig
from src.ai.models.config import ModelsConfig, MODELS_PATH
from src.ai.providers.config import ProvidersConfig, PROVIDERS_PATH
from src.ai.providers.registry import SECRETS
from src.core.base.loader import BaseLoader


class AIConfigLoader(BaseLoader[AIConfig]):

    @classmethod
    def _inject_secrets(cls, ai_config: AIConfig):
        for provider, api_key in SECRETS.items():
            if provider in ai_config.providers:
                ai_config.providers[provider].set_api_key(api_key=api_key)


    @classmethod
    def _load_config[T](cls, path: Path, schema: type[T]) -> T:
        return schema.model_validate(cls.load_yaml(path=path))


    @classmethod
    def load(cls, path: Path | str | None = None) -> AIConfig:
        providers_config = cls._load_config(path=PROVIDERS_PATH, schema=ProvidersConfig)
        models_config = cls._load_config(path=MODELS_PATH, schema=ModelsConfig)
        ai_config = AIConfig(providers=providers_config.providers, models=models_config.models)
        cls._inject_secrets(ai_config=ai_config)

        return ai_config
