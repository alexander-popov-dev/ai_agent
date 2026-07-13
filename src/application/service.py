from src.ai.schemas.idea import GenerateIdeasOutput, GenerateIdeaInput, ImproveIdeaOutput, ImproveIdeaInput
from src.ai.schemas.story import StoryOutput, StoryInput
from src.application.pipeline import ContentPipeline
from src.application.session import Session
from src.database.redis.repositories.base import BaseRepository


class ContentService:
    def __init__(self, pipeline: ContentPipeline, redis_client: BaseRepository) -> None:
        self._pipeline = pipeline
        self._redis_client = redis_client

    async def generate_ideas(self, user_id: int, niche: str) -> GenerateIdeasOutput:
        session = await self._redis_client.get(user_id=user_id)
        session = session if session else Session(niche=niche)
        idea_intput = GenerateIdeaInput(niche=niche, ideas_count=1)
        ideas = await self._pipeline.generate_ideas(schema=idea_intput)

        session.niche = niche
        session.ideas = ideas

        await self._redis_client.save(user_id=user_id, schema=session)

        return ideas

    async def select_idea(self, user_id: int, selected_idea_index: int) -> None:
        session = await self._redis_client.get(user_id=user_id)
        session.selected_idea_index = selected_idea_index
        await self._redis_client.save(user_id=user_id, schema=session)


    async def improve_idea(self, user_id: int, selected_idea_index: int, instruction: str) -> ImproveIdeaOutput:
        session = await self._redis_client.get(user_id=user_id)
        selected_idea = session.ideas.ideas[selected_idea_index]
        schema = ImproveIdeaInput(idea=selected_idea, instructions=instruction)
        improved_idea = await self._pipeline.improve_idea(schema=schema)
        session.selected_idea = improved_idea
        await self._redis_client.save(user_id=user_id, schema=schema)
        return improved_idea

    async def generate_story(self, user_id: int, instruction: str | None = None) -> StoryOutput:
        session = await self._redis_client.get(user_id=user_id)
        selected = session.selected_idea
        story_input = StoryInput(idea=selected, instruction=instruction)
        story = await self._pipeline.generate_story(schema=story_input)

        session.story = story

        await self._redis_client.save(user_id=user_id, schema=session)

        return story