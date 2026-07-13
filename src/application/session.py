from pydantic import BaseModel, computed_field

from src.ai.schemas.idea import GenerateIdeaOutput, GenerateIdeasOutput

from src.ai.schemas.story import StoryOutput


class Session(BaseModel):
    niche: str
    ideas: GenerateIdeasOutput | None = None
    selected_idea_index: int | None = None
    story: StoryOutput | None = None

    @computed_field
    @property
    def selected_idea(self) -> GenerateIdeaOutput | None:
        if self.ideas and self.selected_idea_index is not None:
            return self.ideas.ideas[self.selected_idea_index]
        return None