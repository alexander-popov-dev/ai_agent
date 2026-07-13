from src.ai.agents.ideas import GenerateIdeasAgent, ImproveIdeaAgent
from src.ai.agents.story import StoryAgent
from src.ai.schemas.idea import GenerateIdeaInput, GenerateIdeasOutput, ImproveIdeaInput, ImproveIdeaOutput
from src.ai.schemas.story import StoryInput, StoryOutput


class ContentPipeline:
    def __init__(
            self,
            ideas_agent: GenerateIdeasAgent,
            improve_idea_agent: ImproveIdeaAgent,
            story_agent: StoryAgent
    ) -> None:
        self._ideas_agent = ideas_agent
        self._improve_agent = improve_idea_agent
        self._story_agent = story_agent


    async def generate_ideas(self, schema: GenerateIdeaInput) -> GenerateIdeasOutput:
        return await self._ideas_agent.execute(schema=schema)


    async def improve_idea(self, schema: ImproveIdeaInput) -> ImproveIdeaOutput:
        return await self._improve_agent.execute(schema=schema)


    async def generate_story(self, schema: StoryInput) -> StoryOutput:
        return await self._story_agent.execute(schema=schema)
