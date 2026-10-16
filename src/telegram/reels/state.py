from uuid import UUID

from pydantic import BaseModel, Field


class ReelsState(BaseModel):

    user_id: UUID
    niche: str
    language: str = "ua"

    ideas: list[str] = Field(default_factory=list)
    selected_idea: str | None = None
    story: str | None = None
    idea_instruction: list[str] = Field(default_factory=list)
    story_instruction: list[str] = Field(default_factory=list)
    is_approved: bool = Field(default_factory=bool)
