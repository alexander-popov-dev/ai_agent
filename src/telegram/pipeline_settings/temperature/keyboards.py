from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram.common.keyboards import add_back_button
from src.telegram.pipeline_settings.context import SettingsAction
from src.telegram.pipeline_settings.callbacks import SettingsCallback


def temperature_keyboards(action: SettingsAction):
    builder = InlineKeyboardBuilder()

    buttons = [
        "0",
        "0.1",
        "0.2",
        "0.3",
        "0.4",
        "0.5",
        "0.6",
        "0.7",
        "0.8",
        "0.9",
        "1",
    ]
    for button in buttons:
        builder.button(
            text=button,
            callback_data=SettingsCallback(
                action=SettingsAction.SAVE_TEMPERATURE,
                object_id=button,
            ).pack(),
        )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=SettingsCallback(action=action))

    return builder.as_markup()
