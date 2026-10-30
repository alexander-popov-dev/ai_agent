from typing import Annotated
from uuid import UUID

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.pipeline.schemas import UserStepSettingsUpdateSchema
from src.application.pipeline.service import PipelineService
from src.telegram.pipeline_settings.context import SettingsAction, SettingsScope, SettingsContext
from src.telegram.pipeline_settings.step.keyboards import step_keyboards
from src.telegram.common.context import get_context, save_context
from src.telegram.pipeline_settings.callbacks import SettingsCallback

router = Router(name="settings_step")
actions = [
    SettingsAction.SELECT_PIPELINE,
    SettingsAction.SAVE_MODEL,
    SettingsAction.SAVE_TEMPERATURE
]


@router.callback_query(SettingsCallback.filter(F.action.in_(actions)))
@inject
async def show_steps_screen(
        callback: CallbackQuery,
        callback_data: SettingsCallback,
        state: FSMContext,
        pipeline_service: Annotated[PipelineService, FromDishka()],
) -> None:
    await callback.answer()
    context = await get_context(state=state, context_cls=SettingsContext)
    callback_object = callback_data.object_id

    text = f"<b>Выбери шаг</b>\n\n"

    if SettingsAction.SELECT_PIPELINE == callback_data.action:
        context.pipeline_id = UUID(callback_object) if callback_object else context.pipeline_id

    elif SettingsAction.SAVE_MODEL == callback_data.action:
        await save_model(context=context, service=pipeline_service, model_id=UUID(callback_data.object_id))
        text += f"<i>Модель сохранена</i>\n\n"

    elif SettingsAction.SAVE_TEMPERATURE == callback_data.action:
        await save_temperature(context=context, service=pipeline_service, temperature=float(callback_data.object_id))
        text += f"<i>Температура сохранена</i>\n\n"

    user_steps = await pipeline_service.get_user_pipeline_settings(pipeline_id=context.pipeline_id, user_id=context.user_id)
    context.step_id = None
    context.provider_id = None
    context.model_id = None
    context.action = SettingsAction.SELECT_STEP

    await save_context(context=context, state=state)

    for step in user_steps:
        if step.user_settings:
            model = step.user_settings.model.display_name
            temperature = step.user_settings.temperature
        else:
            model = "Нет"
            temperature = "Нет"

        text += (f"<b>Шаг:</b> {step.display_name}\n"
                 f"<b>Модель:</b> {model}\n"
                 f"<b>Температура:</b> {temperature}\n\n")

    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text=text,
            reply_markup=step_keyboards(steps=user_steps)
        )

async def save_model(context: SettingsContext, model_id: UUID,  service: PipelineService) -> None:
    if SettingsScope.STEP == context.scope:
        setting = UserStepSettingsUpdateSchema(
            user_id=context.user_id,
            step_id=context.step_id,
            model_id=model_id,
        )
        await service.upsert_settings(settings=[setting])

    elif SettingsScope.PIPELINE == context.scope:
        steps = await service.get_pipeline_steps(pipeline_id=context.pipeline_id)
        settings = [
            UserStepSettingsUpdateSchema(
                user_id=context.user_id,
                step_id=step.id,
                model_id=model_id,
            )
            for step in steps
        ]
        await service.upsert_settings(settings=settings)

async def save_temperature(context: SettingsContext, temperature: float,  service: PipelineService) -> None:
    if SettingsScope.STEP == context.scope:
        setting = UserStepSettingsUpdateSchema(
            user_id=context.user_id,
            step_id=context.step_id,
            temperature=temperature,
        )
        await service.upsert_settings(settings=[setting])

    elif SettingsScope.PIPELINE == context.scope:
        steps = await service.get_pipeline_steps(pipeline_id=context.pipeline_id)
        settings = [
            UserStepSettingsUpdateSchema(
                user_id=context.user_id,
                step_id=step.id,
                temperature=temperature,
            )
            for step in steps
        ]
        await service.upsert_settings(settings=settings)