from enum import StrEnum


class Agent(StrEnum):
    GENERATE_IDEAS = "generate_ideas"
    GENERATE_STORY = "generate_story"
    EDIT_STORY = "edit_story"
    PARSE_USER_ANSWER = "parse_user_answer"


class StoryEditStatus(StrEnum):
    EDIT = "edit"
    APPROVED = "approved"