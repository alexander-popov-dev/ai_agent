from pydantic import BaseModel, computed_field, Field

from src.pipelines.reels.idea.schemas import GenerateIdeaOutput, IdeaContext
from src.pipelines.reels.story.schemas import GenerateStoryOutput, StoryContext, ParseUserAnswerContext


class ReelsSessionConfig(BaseModel):
    niche: str
    ideas: list[GenerateIdeaOutput] = Field(default_factory=list)
    selected_idea_index: int | None = None
    story: GenerateStoryOutput | None = None
    idea_context: IdeaContext = Field(default_factory=IdeaContext)
    story_context: StoryContext = Field(default_factory=StoryContext)
    user_answer_context: ParseUserAnswerContext = Field(default_factory=ParseUserAnswerContext)


    def set_niche(self, niche: str) -> None:
        self.niche = niche

    def add_ideas(self, ideas: list[GenerateIdeaOutput]) -> None:
        self.ideas.extend(ideas)

    def add_idea_instruction(self, instructions: str | None) -> None:
        if instructions is not None:
            self.idea_context.instructions.append(instructions)

    def set_selected_idea(self, selected_idea_index: int) -> None:
        self.selected_idea_index = selected_idea_index

    def clear_ideas_instructions(self) -> None:
        self.idea_context.instructions.clear()

    def add_story_instruction(self, instructions: str | None) -> None:
        if instructions is not None:
            self.story_context.instructions.append(instructions)

    def set_story(self, story: GenerateStoryOutput) -> None:
        self.story = story

    def set_parsed_scenes(self, scenes: list[int]) -> None:
        self.user_answer_context.scenes = scenes

    def set_parsed_instruction(self, instruction: str | None) -> None:
        if instruction is not None:
            self.user_answer_context.instruction = instruction

    @computed_field
    @property
    def selected_idea(self) -> GenerateIdeaOutput | None:
        if self.ideas and self.selected_idea_index is not None:
            return self.ideas[self.selected_idea_index]
        return None
