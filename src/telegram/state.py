from aiogram.fsm.state import State, StatesGroup


class ReelsStates(StatesGroup):
    waiting_more_ideas = State()
    waiting_story_edit = State()