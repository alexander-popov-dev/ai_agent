from pathlib import Path

from src.core.base.loader import BaseLoader
from src.pipelines.reels.config import ReelsPipelineConfig, PIPELINE_CONFIG_PATH


class ReelsPipelineConfigLoader(BaseLoader):
    @classmethod
    def load(cls, path: Path | str | None = None) -> ReelsPipelineConfig:
        config = cls.load_yaml(path=PIPELINE_CONFIG_PATH)
        return ReelsPipelineConfig.model_validate(config)
