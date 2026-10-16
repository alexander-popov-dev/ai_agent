from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.ai.schemas import AIProviderSchema
from src.pipelines.reels.enums import Callback


def providers_keyboards(providers: list[AIProviderSchema]):
    kb = InlineKeyboardBuilder()

    for provider in providers:
        kb.button(
            text=provider.display_name,
            callback_data=f"{Callback.PROVIDER}{provider.id}",
        )
    kb.adjust(1)

    return kb.as_markup()
