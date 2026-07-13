from pydantic import BaseModel


class GenerateIdeaInput(BaseModel):
    niche: str
    language: str = "ru"
    ideas_count: int = 10


class GenerateIdeaOutput(BaseModel):
    title: str
    description: str


class GenerateIdeasOutput(BaseModel):
    ideas: list[GenerateIdeaOutput]


class ImproveIdeaInput(BaseModel):
    idea: GenerateIdeaOutput
    instructions: str


class ImproveIdeaOutput(BaseModel):
    idea: GenerateIdeaInput
    instructions: str
