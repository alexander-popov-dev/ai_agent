from pydantic import BaseModel

from src.ai.schemas.idea import GenerateIdeaOutput


class StoryInput(BaseModel):
    idea: GenerateIdeaOutput
    instruction: str | None = None


class StoryScene(BaseModel):
    order: int
    narration: str
    visual_description: str


class StoryOutput(BaseModel):
    title: str
    scenes: list[StoryScene]


class EditStoryInput(BaseModel):
    instruction: str


class EditStoryOutput(BaseModel):
    regenerate: bool
    scenes: list[int] = Field(default_factory=list)
    instruction: str
