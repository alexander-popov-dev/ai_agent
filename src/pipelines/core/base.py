from src.core.logging.mixin import LoggedMixin


class BasePipeline(LoggedMixin):
    __log_layer__ = "pipeline"