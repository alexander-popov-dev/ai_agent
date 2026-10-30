from uuid import UUID

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import inject


from src.telegram.reels.language.keyboards import language_keyboard
from src.telegram.common.context import get_context, save_context
from src.telegram.reels.context import ReelsContext, ReelsAction
from src.telegram.reels.callbacks import ReelsCallback

router = Router(name="reels_language")


@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.SELECT_NICHE))
@inject
async def show_language_screen(
        callback: CallbackQuery,
        callback_data: ReelsCallback,
        state: FSMContext
) -> None:
    await callback.answer()
    niche_id = callback_data.object_id

    context = await get_context(state=state, context_cls=ReelsContext)

    if niche_id:
        context.niche_id = UUID(niche_id)

    await save_context(context=context, state=state)

    await callback.message.edit_text(
        text="Выбери язык",
        reply_markup=language_keyboard()
    )
