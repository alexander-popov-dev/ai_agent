from src.ai.agent.base import BaseAgent
from src.core.logging.decorators import log_execution
from src.pipelines.core.base import BasePipeline
from src.pipelines.reels.critic.schemas import CritiqueStoryInput, CritiqueStoryOutput
from src.pipelines.reels.idea.schemas import GenerateIdeaInput, GenerateIdeasOutput
from src.pipelines.reels.story.schemas import GenerateStoryInput, GenerateStoryOutput, EditStoryInput


class ReelsPipeline(BasePipeline):

    def __init__(
            self,
            generate_ideas: BaseAgent,
            generate_story: BaseAgent,
            edit_story: BaseAgent,
            critique_story: BaseAgent,
    ) -> None:
        self._generate_ideas = generate_ideas
        self._generate_story = generate_story
        self._edit_story = edit_story
        self._critique_story = critique_story

    @log_execution
    async def generate_ideas(self, payload: GenerateIdeaInput) -> GenerateIdeasOutput:
        return await self._generate_ideas.execute(payload=payload)

    @log_execution
    async def generate_story(self, payload: GenerateStoryInput) -> GenerateStoryOutput:
        return await self._generate_story.execute(payload=payload)

    @log_execution
    async def edit_story(self, payload: EditStoryInput) -> GenerateStoryOutput:
        return await self._edit_story.execute(payload=payload)

    @log_execution
    async def critique_story(self, payload: CritiqueStoryInput) -> CritiqueStoryOutput:
        return await self._critique_story.execute(payload=payload)
