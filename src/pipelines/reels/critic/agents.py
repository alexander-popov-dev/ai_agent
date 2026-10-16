from src.ai.agent.base import BaseAgent
from src.pipelines.reels.critic.schemas import CritiqueStoryInput, CritiqueStoryOutput


class CritiqueStoryAgent(BaseAgent[CritiqueStoryInput, CritiqueStoryOutput]):
    agent = "critique_story"
    output_schema = CritiqueStoryOutput
