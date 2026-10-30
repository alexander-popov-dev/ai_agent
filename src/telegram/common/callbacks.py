from aiogram.filters.callback_data import CallbackData


class CommonCallback(CallbackData, prefix="callback"):
    action: str
    object_id: str | int | None = None
