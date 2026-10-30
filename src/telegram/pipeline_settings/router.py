from aiogram import Router

from src.telegram.pipeline_settings.pipeline.handlers import router as pipeline_router
from src.telegram.pipeline_settings.step.handlers import router as step_router
from src.telegram.pipeline_settings.settings.handlers import router as settings_router
from src.telegram.pipeline_settings.provider.handlers import router as provider_router
from src.telegram.pipeline_settings.model.handlers import router as model_router
from src.telegram.pipeline_settings.temperature.handlers import router as temperature_router

router = Router(name="pipeline_settings")

router.include_routers(
    pipeline_router,
    step_router,
    settings_router,
    provider_router,
    model_router,
    temperature_router
)