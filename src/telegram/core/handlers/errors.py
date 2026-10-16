from aiogram import Router
from aiogram.types import ErrorEvent

from src.core.logging.logger import get_logger

logger = get_logger()

router = Router()


@router.errors()
async def errors_handler(event: ErrorEvent):

    logger.exception(
        "Telegram handler failed",
        exception=event.exception,
    )

    if event.update.message:
        await event.update.message.answer(
            "❌ Произошла ошибка.\n"
            "Попробуйте ещё раз."
        )

    elif event.update.callback_query:
        await event.update.callback_query.message.answer(
            "❌ Произошла ошибка.\n"
            "Попробуйте ещё раз."
        )

    return True