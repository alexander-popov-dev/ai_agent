from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from src.core.base.loader import BaseLoader


DEFAULT_USER_MESSAGE = "Please follow the instructions above."

class PromptLoader(BaseLoader):

    @classmethod
    def load(cls, path: Path | str | None = None) -> ChatPromptTemplate:
        prompt =  path.read_text(encoding="utf-8")

        return ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human", DEFAULT_USER_MESSAGE)
            ]
        )