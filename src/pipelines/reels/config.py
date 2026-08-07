from pydantic import BaseModel

from src.paths import BASE_DIR
from src.pipelines.core.config import PipelineConfig
from src.pipelines.core.enums import Pipeline

PIPELINE_CONFIG_PATH = BASE_DIR / "src" / "pipelines" / "reels" / "pipeline_config.yaml"
PROMPTS_PATH = BASE_DIR / "src" / "pipelines" / "reels" / "prompts"

class ReelsPipelineStepsConfig(BaseModel):
    generate_ideas: PipelineConfig
    generate_story: PipelineConfig
    parse_user_answer: PipelineConfig
    edit_story: PipelineConfig


class ReelsPipelineConfig(BaseModel):
    pipelines: dict[Pipeline, ReelsPipelineStepsConfig]