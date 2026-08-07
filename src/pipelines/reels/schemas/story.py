from html import escape

from pydantic import BaseModel, Field

from src.pipelines.reels.schemas.idea import GenerateIdeaOutput
from src.core.enums import Language

MAX_MESSAGE_LENGTH = 4000

class StoryContext(BaseModel):
    instructions: list[str] = []

class ParseUserAnswerContext(BaseModel):
    instruction: str | None = None
    scenes: list[int] = Field(default_factory=list)

class GenerateStoryInput(BaseModel):
    language: Language = Language.UA
    idea: GenerateIdeaOutput
    instructions: StoryContext = Field(default_factory=StoryContext)


class GenerateStoryOutput(BaseModel):
    caption: str
    narration: str

    def to_html(self) -> str:
        return (
            f"<b>🎬 {escape(self.caption)}</b>\n\n"
            f"<b>📖 Повествование</b>\n\n"
            f"{escape(self.narration)}"
        )

class EditStoryInput(BaseModel):
    language: Language = Language.UA
    story: GenerateStoryOutput
    instruction: str

