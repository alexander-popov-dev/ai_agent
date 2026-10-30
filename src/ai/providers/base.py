from abc import ABC, abstractmethod
from typing import ClassVar

from langchain_core.language_models import BaseChatModel

from src.ai.settings import get_ai_project_settings
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema
from src.core.logging.mixin import LoggedMixin


class BaseProvider(ABC, LoggedMixin):

    provider: ClassVar[str]
    _registry: ClassVar[dict[str, type["BaseProvider"]]] = {}

    def __init__(self):
        self._settings = get_ai_project_settings()

    def __init_subclass__(cls, **kwargs) -> None:
        """Automatically registers child agent classes by their `agent` key."""
        super().__init_subclass__(**kwargs)
        if "provider" in cls.__dict__:
            BaseProvider._registry[cls.provider] = cls

    @classmethod
    def get_provider(cls, provider: str) -> type["BaseProvider"]:
        """Retrieve an provider class from the registry by its business key (from DB).

        :param provider: The string identifier matching `pipeline_step.user_settings.provider`.
        :return: Registered BaseProvider subclass.
        :raises ValueError: If the agent key is not registered in memory.
        """
        try:
            return cls._registry[provider]
        except KeyError:
            raise ValueError(f"Provider with key '{provider}' is not registered in Python runtime.")

    @abstractmethod
    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        ...
