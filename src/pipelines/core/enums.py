from enum import StrEnum


class Pipeline(StrEnum):
    REELS = "reels"
    ARTICLES = "articles"


class PipelineSessionStatus(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"
    FAILED = "failed"
