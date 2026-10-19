from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.pipeline.schemas import PipelineSchema
from src.pipelines.reels.enums import Callback


def pipeline_keyboard(pipelines: list[PipelineSchema]):
    kb = InlineKeyboardBuilder()

    for pipeline in pipelines:
        kb.button(
            text=pipeline.display_name,
            callback_data=f"{Callback.PIPELINE}{pipeline.id}",
        )
        kb.adjust(1)
    return kb.as_markup()
