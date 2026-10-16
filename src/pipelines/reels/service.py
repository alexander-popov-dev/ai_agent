from src.pipelines.reels.pipeline import ReelsPipeline
from src.pipelines.reels.idea.schemas import GenerateIdeasOutput, GenerateIdeaInput
from src.pipelines.reels.story.schemas import GenerateStoryOutput, GenerateStoryInput, EditStoryInput
from src.telegram.reels.session.session import ReelsPipelineSession


class ReelsService:
    def __init__(self, pipeline: ReelsPipeline, session: ReelsPipelineSession) -> None:
        self._pipeline = pipeline
        self._session = session

    async def generate_ideas(self, user_id: int, niche: str, ideas_count: int) -> GenerateIdeasOutput:
        await self._session.delete_session(user_id=user_id)
        session = await self._session.get_session(user_id=user_id, niche=niche)
        idea_input = GenerateIdeaInput(niche=niche, ideas_count=ideas_count)
        ideas = await self._pipeline.generate_ideas(schema=idea_input)
        session.set_niche(niche=niche)
        session.add_ideas(ideas=ideas.ideas)
        await self._session.save_session(user_id=user_id, session=session)
        return ideas

    async def generate_more_ideas(
            self, user_id: int,
            instruction: str,
            ideas_count: int,
    ) -> GenerateIdeasOutput:
        session = await self._session.get_session(user_id=user_id)
        session.add_idea_instruction(instructions=instruction)
        idea_input = GenerateIdeaInput(
            niche=session.niche,
            ideas_count=ideas_count,
            ideas=session.ideas,
            instructions=session.idea_context,
        )
        ideas = await self._pipeline.generate_ideas(schema=idea_input)
        session.add_ideas(ideas=ideas.ideas)
        await self._session.save_session(user_id=user_id, session=session)
        return ideas

    async def select_idea(self, user_id: int, selected_idea_index: int) -> None:
        session = await self._session.get_session(user_id=user_id)
        session.set_selected_idea(selected_idea_index=selected_idea_index)
        session.clear_ideas_instructions()
        await self._session.save_session(user_id=user_id, session=session)


    async def generate_story(self, user_id: int, instruction: str | None = None) -> GenerateStoryOutput:
        session = await self._session.get_session(user_id=user_id)
        session.add_story_instruction(instructions=instruction)
        story_input = GenerateStoryInput(idea=session.selected_idea, instructions=session.story_context)
        story = await self._pipeline.generate_story(schema=story_input)
        session.set_story(story=story)
        await self._session.save_session(user_id=user_id, session=session)
        return story


    async def edit_story(self, user_id: int, instruction: str) -> GenerateStoryOutput:
        session = await self._session.get_session(user_id=user_id)
        session.add_story_instruction(instructions=instruction)
        edit_story_input = EditStoryInput(
            story=session.story,
            instruction=instruction,
        )
        edited_story = await self._pipeline.edit_story(schema=edit_story_input)
        session.set_story(story=edited_story)
        await self._session.save_session(user_id=user_id, session=session)
        return edited_story


    async def approve_story(self, user_id: int) -> None:
        await self._session.delete_session(user_id=user_id)


    async def get_ideas_count(self, user_id: int) -> int:
        session = await self._session.get_session(user_id=user_id)
        return len(session.ideas)