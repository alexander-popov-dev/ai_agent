from html import escape
from typing import Annotated

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.niche.service import NicheService
from src.core.enums import Language
from src.pipelines.reels.workflow.decisions import ChooseIdeaDecision, ChooseIdeaAction
from src.pipelines.reels.workflow.service import ReelsPipelineService
from src.telegram.common.context import get_context, save_context
from src.telegram.reels.context import ReelsAction, ReelsContext
from src.telegram.reels.idea.keyboards import ideas_keyboard
from src.telegram.reels.callbacks import ReelsCallback
from src.telegram.reels.state import ReelsState

router = Router(name="reels_idea")

IDEAS_COUNT: int = 10


@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.SELECT_LANGUAGE))
@inject
async def show_ideas_screen(
        callback: CallbackQuery,
        callback_data: ReelsCallback,
        reels_service: Annotated[ReelsPipelineService, FromDishka()],
        niche_service: Annotated[NicheService, FromDishka()],
        state: FSMContext
) -> None:
    await callback.answer(text="Ща! Погодь")
    context = await get_context(state=state, context_cls=ReelsContext)
    await clear_idea_messages(target=callback, idea_message_ids=context.idea_message_ids)
    niche = await niche_service.get_niche(niche_id=context.niche_id)
    language = callback_data.object_id

    if language:
        context.language = language
    else:
        language = context.language

    await save_context(context=context, state=state)

    response = await reels_service.start(
        user_id=context.user_id,
        pipeline_id=context.pipeline_id,
        niche=niche.name,
        language=Language(language),
        ideas_count=IDEAS_COUNT,
    )

    context.session_id = response.session_id

    context.idea_message_ids = await render_ideas_message(
        target=callback,
        ideas=response.state.ideas,
    )

    await save_context(context=context, state=state)


@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.MORE_IDEAS))
async def more_ideas(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReelsState.waiting_more_ideas)
    context = await get_context(state=state, context_cls=ReelsContext)
    await clear_idea_messages(target=callback, idea_message_ids=context.idea_message_ids)
    await callback.message.answer(text="Напишите что изменить", reply_markup=None)


@router.message(ReelsState.waiting_more_ideas)
@inject
async def show_more_ideas_screen(
        message: Message,
        reels_service: Annotated[ReelsPipelineService, FromDishka()],
        state: FSMContext,
) -> None:
    context = await get_context(state=state, context_cls=ReelsContext)

    response = await reels_service.resume(
        user_id=context.user_id,
        session_id=context.session_id,
        decision=ChooseIdeaDecision(action=ChooseIdeaAction.regenerate, instruction=message.text),
    )

    context.idea_message_ids = await render_ideas_message(
        target=message,
        ideas=response.state.ideas,
    )

    await save_context(context=context, state=state)


async def render_ideas_message(target: Message | CallbackQuery, ideas: list) -> list[int]:
    idea_message_ids = []

    for i, idea in enumerate(ideas):
        text = (
            f"💡 <b>Идея {i + 1}</b>\n\n"
            f"<b>📌 Название</b>\n"
            f"{escape(idea.title)}\n\n"
            f"<b>📝 Описание</b>\n"
            f"{escape(idea.description)}"
        )

        keyboard = ideas_keyboard(idea_index=i, is_more_btn=i == len(ideas) - 1)

        if isinstance(target, Message):
            msg = await target.answer(
                text=text,
                reply_markup=keyboard,
            )
        else:
            msg = await target.message.answer(
                text=text,
                reply_markup=keyboard,
            )

        idea_message_ids.append(msg.message_id)

    return idea_message_ids


async def clear_idea_messages(target: Message | CallbackQuery, idea_message_ids: list[int]) -> None:
    if idea_message_ids:
        if isinstance(target, Message):
            await target.bot.delete_messages(chat_id=target.chat.id, message_ids=idea_message_ids)
        if isinstance(target, CallbackQuery):
            await target.bot.delete_messages(chat_id=target.message.chat.id, message_ids=idea_message_ids)
