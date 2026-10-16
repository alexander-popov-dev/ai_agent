from pydantic import BaseModel, Field

from src.core.enums import Language


class CritiqueStoryInput(BaseModel):
    caption: str
    narration: str
    language: Language = Language.UA


class CritiqueStoryOutput(BaseModel):
    summary: str = Field(description="Short overall assessment of the narration")
    issues: list[str] = Field(default_factory=list, description="Concrete problems to improve")
    is_acceptable: bool = Field(description="Whether the story meets the quality criteria")
