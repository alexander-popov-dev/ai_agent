from aiogram.filters.callback_data import CallbackData


class ReelsCallback(CallbackData, prefix="reels"):
    action: str
    object_id: str | int | None = None