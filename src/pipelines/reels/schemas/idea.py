from pydantic import BaseModel, Field

from src.core.enums import Language


class IdeaContext(BaseModel):
    instructions: list[str] = []


class GenerateIdeaOutput(BaseModel):
    title: str
    description: str


class GenerateIdeaInput(BaseModel):
    niche: str
    language: Language = Language.UA
    ideas_count: int = 10
    ideas: list[GenerateIdeaOutput] = []
    instructions: IdeaContext = Field(default_factory=IdeaContext)


class GenerateIdeasOutput(BaseModel):
    ideas: list[GenerateIdeaOutput]
