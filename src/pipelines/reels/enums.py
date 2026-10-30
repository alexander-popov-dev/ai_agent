from enum import StrEnum


class ReelsAgent(StrEnum):
    GENERATE_IDEAS = "generate_ideas"
    GENERATE_STORY = "generate_story"
    EDIT_STORY = "edit_story"
    CRITIQUE_STORY = "critique_story"
