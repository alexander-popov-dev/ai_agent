from src.ai.base.agent import BaseAgent
from src.core.logging.decorators import log_execution
from src.pipelines.core.base import BasePipeline
from src.pipelines.reels.schemas.idea import GenerateIdeaInput, GenerateIdeasOutput
from src.pipelines.reels.schemas.story import GenerateStoryInput, GenerateStoryOutput, EditStoryInput


class ReelsPipeline(BasePipeline):

    def __init__(
            self,
            generate_ideas: BaseAgent,
            generate_story: BaseAgent,
            edit_story: BaseAgent,
    ) -> None:
        self._generate_ideas = generate_ideas
        self._generate_story = generate_story
        self._edit_story = edit_story


    @log_execution
    async def generate_ideas(self, schema: GenerateIdeaInput) -> GenerateIdeasOutput:
        return await self._generate_ideas.execute(schema=schema)


    @log_execution
    async def generate_story(self, schema: GenerateStoryInput) -> GenerateStoryOutput:
        return await self._generate_story.execute(schema=schema)


    @log_execution
    async def edit_story(self, schema: EditStoryInput) -> GenerateStoryOutput:
        return await self._edit_story.execute(schema=schema)
