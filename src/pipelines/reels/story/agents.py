from src.ai.agent.base import BaseAgent
from src.pipelines.reels.story.schemas import GenerateStoryInput, GenerateStoryOutput, EditStoryInput


class GenerateStoryAgent(BaseAgent[GenerateStoryInput, GenerateStoryOutput]):
    agent = "generate_story"
    output_schema = GenerateStoryOutput


class EditStoryAgent(BaseAgent[EditStoryInput, GenerateStoryOutput]):
    agent = "edit_story"
    output_schema = GenerateStoryOutput
