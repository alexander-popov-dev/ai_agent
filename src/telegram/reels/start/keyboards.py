from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.niche.schemas import NicheScheme
from src.core.enums import Language


def niche_keyboard(niches: list[NicheScheme]):

    kb = InlineKeyboardBuilder()

    for niche in niches:
        kb.button(
            text=niche.name,
            callback_data=f"niche_{niche.id}",

        )
        kb.adjust(1)
    return kb.as_markup()


def language_keyboard():

    kb = InlineKeyboardBuilder()

    for lang in Language:
        kb.button(
            text=lang.name,
            callback_data=f"lang_{lang.value}",

        )
        kb.adjust(1)
    return kb.as_markup()