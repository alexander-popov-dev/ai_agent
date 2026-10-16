from functools import cached_property
from typing import Any, ClassVar

from deepagents import create_deep_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from src.core.logging.mixin import LoggedMixin


class BaseAgent[TInput: BaseModel, TOutput: BaseModel](LoggedMixin):
    """Base class for typed LLM agents with automatic registry discovery.

    Subclasses must specify `agent` and `output_schema`.
    """

    agent: ClassVar[str]
    output_schema: ClassVar[type[BaseModel]]

    _registry: ClassVar[dict[str, type["BaseAgent[Any, Any]"]]] = {}

    def __init__(self, model: BaseChatModel, prompt: ChatPromptTemplate) -> None:
        """Initialize the agent with an LLM and a prompt template."""
        self._model = model
        self._prompt = prompt

    def __init_subclass__(cls, **kwargs) -> None:
        """Automatically registers child agent classes by their `agent` key."""
        super().__init_subclass__(**kwargs)
        if "agent" in cls.__dict__:
            BaseAgent._registry[cls.agent] = cls

    @classmethod
    def get_agent(cls, agent: str) -> type["BaseAgent[Any, Any]"]:
        """Retrieve an agent class from the registry by its business key (from DB).

        :param agent: The string identifier matching `pipeline_step.agent`.
        :return: Registered BaseAgent subclass.
        :raises ValueError: If the agent key is not registered in memory.
        """
        try:
            return cls._registry[agent]
        except KeyError:
            raise ValueError(f"Agent with key '{agent}' is not registered in Python runtime.")

    @cached_property
    def _chain(self) -> Runnable:
        """Build and cache the prompt-to-structured-output chain."""
        agent = create_deep_agent()
        return (
            self._prompt
            | self._model.with_structured_output(schema=self.output_schema)
        )

    async def execute(self, payload: TInput) -> TOutput:
        """Execute the agent chain with the given validated input payload.

        :param payload: Pydantic TInput model matching input_schema.
        :return: Structured response matching output_schema (TOutput).
        """
        self.logger.info("Invoking LLM agent", agent=self.agent)
        return await self._chain.ainvoke(payload.model_dump())