from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.pipeline.schemas import PipelineStepSchema
from src.pipelines.reels.enums import Callback


def step_keyboards(steps: list[PipelineStepSchema]):
    kb = InlineKeyboardBuilder()

    for step in steps:
        kb.button(
            text=step.display_name,
            callback_data=f"{Callback.STEP}{step.id}",
        )

    kb.button(text="Для всех", callback_data=f"{Callback.STEP}")

    kb.adjust(1)

    return kb.as_markup()
