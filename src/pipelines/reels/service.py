from src.pipelines.reels.pipeline import ReelsPipeline
from src.pipelines.reels.schemas.idea import GenerateIdeasOutput, GenerateIdeaInput
from src.pipelines.reels.schemas.story import GenerateStoryOutput, GenerateStoryInput, ParseUserAnswerOutput, \
    ParseUserAnswerInput, EditStoryInput
from src.pipelines.reels.session.session import ReelsPipelineSession


class ReelsService:
    def __init__(self, pipeline: ReelsPipeline, session: ReelsPipelineSession) -> None:
        self._pipeline = pipeline
        self._session = session

    async def generate_ideas(self, user_id: int, niche: str, ideas_count: int) -> GenerateIdeasOutput:
        await self._session.delete_session(user_id=user_id)
        session = await self._session.get_session(user_id=user_id, niche=niche)
        idea_intput = GenerateIdeaInput(niche=niche, ideas_count=ideas_count)
        ideas = await self._pipeline.generate_ideas(schema=idea_intput)
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


    async def parse_user_answer(self, user_id: int, answer: str) -> ParseUserAnswerOutput:
        session = await self._session.get_session(user_id=user_id)
        answer_input = ParseUserAnswerInput(instruction=answer)
        parsed_answer = await self._pipeline.parse_user_answer(schema=answer_input)
        session.set_parsed_scenes(scenes=parsed_answer.scenes)
        session.set_parsed_instruction(instruction=parsed_answer.instruction)
        await self._session.save_session(user_id=user_id, session=session)
        return parsed_answer


    async def edit_story(self, user_id: int) -> GenerateStoryOutput:
        session = await self._session.get_session(user_id=user_id)
        selected_scenes = session.selected_scenes
        edit_story_input = EditStoryInput(
            story=session.story,
            scenes=selected_scenes,
            instruction=session.user_answer_context.instruction,
        )
        edited_story = await self._pipeline.edit_story(schema=edit_story_input)
        session.set_edited_scene(scenes=edited_story.scenes)
        await self._session.save_session(user_id=user_id, session=session)
        return session.story


    async def approve_story(self, user_id: int) -> None:
        await self._session.delete_session(user_id=user_id)