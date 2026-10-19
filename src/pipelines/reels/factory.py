from ai.agent.base import BaseAgent
from pipelines.core.config import PipelineConfig
from ai import AIConfig
from ai import ProviderFactory
from src.pipelines.core.enums import Pipeline
from src.pipelines.core.prompt_loader import PromptLoader
from src.pipelines.reels.idea.agents import GenerateIdeasAgent
from src.pipelines.reels.story.agents import GenerateStoryAgent, EditStoryAgent
from src.pipelines.reels.config import ReelsPipelineConfig
from src.pipelines.reels.pipeline import ReelsPipeline


class ReelsPipelineFactory:
    """Factory for creating the Reels pipeline and its agents."""

    @staticmethod
    def create(ai_config: AIConfig, pipelines: ReelsPipelineConfig) -> ReelsPipeline:
        """Create a configured Reels pipeline."""
        reels_config = pipelines.pipelines[Pipeline.REELS]

        return ReelsPipeline(
            generate_ideas=ReelsPipelineFactory._create(
                agent=GenerateIdeasAgent,
                ai_config=ai_config,
                pipeline=reels_config.generate_ideas,
            ),
            generate_story=ReelsPipelineFactory._create(
                agent=GenerateStoryAgent,
                ai_config=ai_config,
                pipeline=reels_config.generate_story,
            ),
            edit_story=ReelsPipelineFactory._create(
                agent=EditStoryAgent,
                ai_config=ai_config,
                pipeline=reels_config.edit_story,
            ),
        )

    @staticmethod
    def _create(agent: type[BaseAgent], ai_config: AIConfig, pipeline: PipelineConfig) -> BaseAgent:
        """Create an agent with its configured model and prompt."""
        return agent(
            model=ProviderFactory.create(
                ai_config=ai_config,
                pipeline_config=pipeline,
            ),
            prompt=PromptLoader.load(path=agent.prompt_path),
        )
