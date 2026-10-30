from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.ai.schemas import AIProviderSchema
from src.telegram.common.keyboards import add_back_button
from src.telegram.pipeline_settings.context import SettingsAction
from src.telegram.pipeline_settings.callbacks import SettingsCallback


def providers_keyboards(providers: list[AIProviderSchema], action: SettingsAction) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for provider in providers:
        builder.button(
            text=provider.display_name,
            callback_data=SettingsCallback(
                action=SettingsAction.SELECT_MODEL,
                object_id=str(provider.id),
            ).pack(),
        )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=SettingsCallback(action=action)
    )

    return builder.as_markup()
