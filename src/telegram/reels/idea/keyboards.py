from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram.reels.context import ReelsAction
from src.telegram.reels.callbacks import ReelsCallback


def ideas_keyboard(idea_index: int, is_more_btn: bool = False) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"✅ Выбрать",
        callback_data=ReelsCallback(
            action=ReelsAction.SELECT_IDEA,
            object_id=idea_index,
        ),
    )

    if is_more_btn:
        builder.button(
            text="➕ Еще идеи",
            callback_data=ReelsCallback(action=ReelsAction.MORE_IDEAS)
        ).adjust(1)

    return builder.as_markup()