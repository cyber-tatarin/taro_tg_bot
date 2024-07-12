from typing import Any, Awaitable, Callable
from aiogram import types
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware

from src.utils.database.uow import UoW


class UoWSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        uow = UoW()
        data['uow'] = uow
        result = await handler(event, data)
        return result
        
    async def on_post_process_message(self, message: types.Message, data: dict, result):
        del data["uow"]

