from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.pipeline.schemas import PipelineSchema
from src.telegram.reels.context import ReelsAction
from src.telegram.reels.callbacks import ReelsCallback


def pipeline_keyboard(pipelines: list[PipelineSchema]):
    builder = InlineKeyboardBuilder()

    for pipeline in pipelines:
        builder.button(
            text=pipeline.display_name,
            callback_data=ReelsCallback(
                action=ReelsAction.SELECT_PIPELINE,
                object_id=str(pipeline.id),
            ),
        )

    builder.adjust(1)

    return builder.as_markup()
