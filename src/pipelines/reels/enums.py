from enum import StrEnum


class Agent(StrEnum):
    GENERATE_IDEAS = "generate_ideas"
    GENERATE_STORY = "generate_story"
    EDIT_STORY = "edit_story"


class Callback(StrEnum):
    PIPELINE = "pipeline"
    NICHE = "niche_"
    LANGUAGE = "language_"
    STEP = "step_"
    FOR_ALL = "for_all"
    PROVIDER = "provider_"
    MODEL = "model_"