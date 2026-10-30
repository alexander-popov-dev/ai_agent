from aiogram.fsm.context import FSMContext
from pydantic import BaseModel


async def get_context[T: BaseModel](state: FSMContext, context_cls: type[T]) -> T:
    data = await state.get_data()
    raw_context = data.get(context_cls.__name__, {})
    return context_cls.model_validate(raw_context)


async def save_context(context: BaseModel, state: FSMContext) -> None:
    await state.update_data(
        {type(context).__name__: context.model_dump(mode="json")}
    )