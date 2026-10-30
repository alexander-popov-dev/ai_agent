from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.niche.schemas import NicheScheme
from src.telegram.common.keyboards import add_back_button
from src.telegram.reels.context import ReelsAction
from src.telegram.reels.callbacks import ReelsCallback


def niche_keyboard(niches: list[NicheScheme]):
    builder = InlineKeyboardBuilder()

    for niche in niches:
        builder.button(
            text=niche.name,
            callback_data=ReelsCallback(
                action=ReelsAction.SELECT_NICHE,
                object_id=str(niche.id),
            ),

        )
    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=ReelsCallback(action=ReelsAction.START)
    )

    return builder.as_markup()
