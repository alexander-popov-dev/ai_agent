from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram.common.keyboards import add_back_button
from src.telegram.pipeline_settings.context import SettingsAction
from src.telegram.pipeline_settings.callbacks import SettingsCallback


def settings_keyboards() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Модель",
        callback_data=SettingsCallback(
            action=SettingsAction.SELECT_PROVIDER
        ).pack(),
    )

    builder.button(
        text="Температура",
        callback_data=SettingsCallback(
            action=SettingsAction.SELECT_TEMPERATURE
        ).pack(),
    )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=SettingsCallback(
            action=SettingsAction.SELECT_PIPELINE
        )
    )

    return builder.as_markup()
