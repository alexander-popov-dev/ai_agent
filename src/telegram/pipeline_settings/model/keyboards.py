from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.ai.schemas import AIModelSchema
from src.telegram.common.keyboards import add_back_button
from src.telegram.pipeline_settings.context import SettingsAction
from src.telegram.pipeline_settings.callbacks import SettingsCallback


def model_keyboards(models: list[AIModelSchema]):
    builder = InlineKeyboardBuilder()

    for model in models:
        builder.button(
            text=model.display_name,
            callback_data=SettingsCallback(
                action=SettingsAction.SAVE_MODEL,
                object_id=str(model.id),
            ).pack(),
        )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=SettingsCallback(action=SettingsAction.SELECT_PROVIDER))

    return builder.as_markup()
