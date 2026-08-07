from src.ai.config import AIConfig
from src.ai.providers.factory import ProviderFactory
from src.pipelines.core.enums import Pipeline
from src.pipelines.core.prompt_loader import PromptLoader
from src.pipelines.reels.agents.ideas import GenerateIdeasAgent
from src.pipelines.reels.agents.story import GenerateStoryAgent, EditStoryAgent
from src.pipelines.reels.config import ReelsPipelineConfig
from src.pipelines.reels.pipeline import ReelsPipeline


class ReelsPipelineFactory:

    @classmethod
    def create(cls, ai_config: AIConfig, pipelines: ReelsPipelineConfig) -> ReelsPipeline:
        pipeline = pipelines.pipelines[Pipeline.REELS]
        return ReelsPipeline(
            generate_ideas=GenerateIdeasAgent(
                model=ProviderFactory.create(
                    ai_config=ai_config,
                    pipeline_config=pipeline.generate_ideas
                ),
                prompt=PromptLoader.load(path=GenerateIdeasAgent.PROMPT_PATH),
            ),
            generate_story=GenerateStoryAgent(
                model=ProviderFactory.create(
                    ai_config=ai_config,
                    pipeline_config=pipeline.generate_story
                ),
                prompt=PromptLoader.load(path=GenerateStoryAgent.PROMPT_PATH),
            ),
            edit_story=EditStoryAgent(
                model=ProviderFactory.create(
                    ai_config=ai_config,
                    pipeline_config=pipeline.edit_story
                ),
                prompt=PromptLoader.load(path=EditStoryAgent.PROMPT_PATH)
            )
        )