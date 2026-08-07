from enum import StrEnum


class Callback(StrEnum):
    NICHE = "niche"
    IDEA = "idea"

    MORE_IDEAS = "more_ideas"

    APPROVE_STORY = "approve_story"
    EDIT_STORY = "edit_story"