from langchain_core.language_models import BaseChatModel

from src.ai.providers.base import BaseProvider

from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class ProviderFactory:

    @staticmethod
    def create(pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        provider_cls = BaseProvider.get_provider(provider=pipeline_step.user_settings.model.provider.name)

        return provider_cls().create_chat_model(pipeline_step=pipeline_step)
