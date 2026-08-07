from aiogram import BaseMiddleware

from src.pipelines.reels.service import ReelsService


class ServiceMiddleware(BaseMiddleware):

    def __init__(self, service: ReelsService):
        self._service = service

    async def __call__(self, handler, event, data):
        data["service"] = self._service
        return await handler(event, data)