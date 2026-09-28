from functools import cached_property

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from src.core.logging.mixin import LoggedMixin


class BaseAgent[TInput: BaseModel, TOutput: BaseModel](LoggedMixin):
    """Base class for LLM agents with typed input and structured output."""

    output_schema: type[TOutput]

    def __init__(self, model: BaseChatModel, prompt: ChatPromptTemplate) -> None:
        """Initialize the agent with an LLM and a prompt template."""
        self._model = model
        self._prompt = prompt

        self.logger.info(
            "Initialized",
            model=self._model_name,
            agent=self.__class__.__name__,
        )

    @property
    def _model_name(self) -> str:
        """Return the model name for logging purposes."""
        return (
            getattr(self._model, "model_name", None)
            or getattr(self._model, "model", None)
            or getattr(self._model, "name", None)
            or self._model.__class__.__name__
        )

    @cached_property
    def _chain(self) -> Runnable:
        """Build and cache the prompt-to-structured-output chain."""
        return (
            self._prompt
            | self._model.with_structured_output(
                schema=self.output_schema,
            )
        )

    async def execute(self, schema: TInput) -> TOutput:
        """Execute the agent with the given input schema."""
        self.logger.info(
            "Invoking LLM agent",
            model=self._model_name,
        )
        return await self._chain.ainvoke(schema.model_dump())
