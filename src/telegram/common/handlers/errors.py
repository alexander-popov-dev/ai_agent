from html import escape

from aiogram import Router
from aiogram.types import ErrorEvent, LinkPreviewOptions

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
            text=f"❌ Произошла ошибка. Попробуйте ещё раз.\n"
                 f"{escape(event.exception.__str__())}",
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

    elif event.update.callback_query:
        await event.update.callback_query.message.answer(
            text=f"❌ Произошла ошибка. Попробуйте ещё раз.\n"
                 f"{escape(event.exception.__str__())}",
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

    return True
