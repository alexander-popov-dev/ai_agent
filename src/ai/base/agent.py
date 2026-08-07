import asyncio
import logging
from functools import cached_property
from typing import Any, TypeVar

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from openrouter.errors import ResponseValidationError
from pydantic import BaseModel

from src.core.logging.logger import get_logger
from src.core.logging.mixin import LoggedMixin

logger = get_logger()
TInput = TypeVar(name="TInput", bound=BaseModel)
TOutput = TypeVar(name="TOutput", bound=BaseModel)


class BaseAgent[TInput, TOutput](LoggedMixin):
    __log_layer__ = "agent"

    OUTPUT_SCHEME: type[TOutput] = TOutput

    def __init__(self, model: BaseChatModel, prompt: ChatPromptTemplate):
        self._model = model
        self._prompt = prompt


    @cached_property
    def _chain(self) -> RunnableSerializable[dict[str, Any], TOutput]:
        return (
                self._prompt
                |
                self._model.with_structured_output(schema=self.OUTPUT_SCHEME)
        )

    async def execute(self, schema: TInput) -> TOutput:
        self.logger.info("Invoking LLM", model=self._model)
        for i in range(6):
            try:
                return await self._chain.ainvoke(schema.model_dump())
            except ResponseValidationError as e:
                await asyncio.sleep(2)

        raise Exception('Invoke error')