from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.pipeline.schemas import PipelineStepSchema
from src.telegram.common.keyboards import add_back_button
from src.telegram.pipeline_settings.context import SettingsAction
from src.telegram.pipeline_settings.callbacks import SettingsCallback


def step_keyboards(steps: list[PipelineStepSchema]):
    builder = InlineKeyboardBuilder()

    for step in steps:
        builder.button(
            text=step.display_name,
            callback_data=SettingsCallback(
                action=SettingsAction.SELECT_STEP,
                object_id=str(step.id)
            ).pack(),
        )

    builder.button(
        text="Для всех шагов",
        callback_data=SettingsCallback(
            action=SettingsAction.SELECT_ALL_STEPS,
        ).pack(),
    )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=SettingsCallback(action=SettingsAction.START)
    )

    return builder.as_markup()
