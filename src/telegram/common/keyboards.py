from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_back_button(builder: InlineKeyboardBuilder, callback: CallbackData) -> InlineKeyboardBuilder:
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=callback.pack()
        )
    )
    return builder
