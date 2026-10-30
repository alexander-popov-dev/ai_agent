from typing import Annotated

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.pipelines.reels.critic.schemas import CritiqueStoryOutput
from src.pipelines.reels.story.schemas import GenerateStoryOutput
from src.pipelines.reels.workflow.decisions import ChooseIdeaAction, ChooseIdeaDecision, ReviewStoryAction, \
    ReviewStoryDecision
from src.pipelines.reels.workflow.service import ReelsPipelineService
from src.telegram.common.context import get_context
from src.telegram.reels.context import ReelsAction, ReelsContext
from src.telegram.reels.story.keyboards import story_keyboard
from src.telegram.reels.state import ReelsState
from src.telegram.reels.callbacks import ReelsCallback

router = Router(name="reels_story")

@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.SELECT_IDEA))
@inject
async def show_generate_story_screen(
        callback: CallbackQuery,
        callback_data: ReelsCallback,
        reels_service: Annotated[ReelsPipelineService, FromDishka()],
        state: FSMContext,
) -> None:
    await callback.answer()
    context = await get_context(state=state, context_cls=ReelsContext)
    await callback.bot.delete_messages(chat_id=callback.message.chat.id, message_ids=context.idea_message_ids)

    idea_index = int(callback_data.object_id)

    response = await reels_service.resume(
        session_id=context.session_id,
        user_id=context.user_id,
        decision=ChooseIdeaDecision(action=ChooseIdeaAction.choose, idea_index=idea_index)
    )

    if response.interrupt and response.interrupt.type == "review_story":
        story = response.interrupt.story
        critique = response.interrupt.critique
        text = build_story_text(story=story, critique=critique)

        await callback.message.answer(
            text=text,
            reply_markup=story_keyboard()
        )

@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.EDIT_STORY))
async def show_edit_story_screen(callback: CallbackQuery, state: FSMContext) -> None:

    await state.set_state(ReelsState.waiting_story_edit)

    await callback.message.edit_text(
        text="Что изменить?",
        reply_markup=None
    )


@router.message(ReelsState.waiting_story_edit)
@inject
async def show_edit_story_message_screen(
    message: Message,
    reels_service: Annotated[ReelsPipelineService, FromDishka()],
    state: FSMContext,
) -> None:
    context = await get_context(state=state, context_cls=ReelsContext)

    response = await reels_service.resume(
        session_id=context.session_id,
        user_id=context.user_id,
        decision=ReviewStoryDecision(action=ReviewStoryAction.edit, instruction=message.text)
    )

    if response.interrupt and response.interrupt.type == "review_story":
        story = response.interrupt.story
        critique = response.interrupt.critique
        text = build_story_text(story=story, critique=critique)

        await message.answer(
            text=text,
            reply_markup=story_keyboard()
        )


def build_story_text(story: GenerateStoryOutput,  critique: CritiqueStoryOutput) -> str:
    return (
        f"🎬 <b>{story.caption}</b>\n\n"
        f"<b>📖 Повествование</b>\n\n"
        f"{story.narration}\n\n"
        f"📉 <b>Критика</b>\n"
        f"{critique.summary}\n"
        f"Проблемы: {', '.join(critique.issues) if critique.issues else '—'}"
    )