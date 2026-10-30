from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.pipeline.schemas import PipelineSchema
from src.telegram.pipeline_settings.context import SettingsAction
from src.telegram.pipeline_settings.callbacks import SettingsCallback


def pipeline_keyboard(pipelines: list[PipelineSchema]):
    builder = InlineKeyboardBuilder()

    for pipeline in pipelines:
        builder.button(
            text=pipeline.display_name or pipeline.name,
            callback_data=SettingsCallback(
                action=SettingsAction.SELECT_PIPELINE,
                object_id=str(pipeline.id),
            ).pack(),
        )

    builder.adjust(1)

    return builder.as_markup()
