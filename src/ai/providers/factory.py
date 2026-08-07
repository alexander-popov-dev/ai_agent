from langchain_core.language_models import BaseChatModel

from src.ai.config import AIConfig
from src.ai.providers.registry import PROVIDERS
from src.pipelines.core.config import PipelineConfig


class ProviderFactory:

    @staticmethod
    def create(ai_config: AIConfig, pipeline_config: PipelineConfig) -> BaseChatModel:
        model = ai_config.models[pipeline_config.model]
        provider = ai_config.providers[model.provider]

        provider_cls = PROVIDERS.get(provider.provider)

        if provider_cls is None:
            raise ValueError(f"Provider {provider} is not supported")

        return provider_cls().create_chat_model(
            provider_config=provider,
            model_config=model,
            pipeline_config=pipeline_config
        )
