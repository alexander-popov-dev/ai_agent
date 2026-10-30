from typing import Annotated
from uuid import UUID

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.niche.service import NicheService
from src.application.user.service import UserService

from src.telegram.reels.niche.keyboards import niche_keyboard
from src.telegram.common.context import save_context, get_context
from src.telegram.reels.context import ReelsContext, ReelsAction
from src.telegram.reels.callbacks import ReelsCallback

router = Router(name="reels_niche")


@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.SELECT_PIPELINE))
@inject
async def show_niche_screen(
        callback: CallbackQuery,
        callback_data: ReelsCallback,
        user_service: Annotated[UserService, FromDishka()],
        niche_service: Annotated[NicheService, FromDishka()],
        state: FSMContext,
) -> None:
    pipeline_id = callback_data.object_id

    context = await get_context(state=state, context_cls=ReelsContext)

    if pipeline_id:
        context.pipeline_id = UUID(pipeline_id)

    context.niche_id = None
    await save_context(state=state, context=context)

    user = await user_service.get_by_external_id(external_id=str(callback.from_user.id))
    niches = await niche_service.get_all_by_user(user_id=user.id)

    await callback.message.edit_text(
        text="<b>Выбери тему</b>",
        reply_markup=niche_keyboard(niches=niches)
    )
