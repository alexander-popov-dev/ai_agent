from abc import ABC
from functools import cached_property
from typing import Any, TypeVar

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel

from src.ai.loaders.prompt import PromptLoader

TInput = TypeVar(name="TInput", bound=BaseModel)
TOutput = TypeVar(name="TOutput", bound=BaseModel)


class BaseAgent[TInput, TOutput](ABC):
    PROMPT_NAME: str
    OUTPUT_SCHEME: type[TOutput]

    def __init__(self, llm: BaseChatModel):
        self._llm = llm
        self._prompt = self._create_prompt()

    def _create_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    PromptLoader.load(self.PROMPT_NAME),
                )
            ]
        )

    @cached_property
    def _chain(self) -> RunnableSerializable[dict[str, Any], dict[str, Any]]:
        return (
                self._prompt
                |
                self._llm.with_structured_output(schema=self.OUTPUT_SCHEME)
        )

    async def execute(self, schema: TInput) -> TOutput:
        return await self._chain.ainvoke(schema.model_dump())
