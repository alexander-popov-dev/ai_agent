from aiogram.fsm.state import StatesGroup, State


class PipelineSettingsStep(StatesGroup):
    pipeline = State()
    user = State()
