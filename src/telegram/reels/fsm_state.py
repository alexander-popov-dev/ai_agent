from aiogram.fsm.state import State, StatesGroup


class ReelsState(StatesGroup):
    waiting_niches = State()
    waiting_more_ideas = State()
    waiting_story_edit = State()