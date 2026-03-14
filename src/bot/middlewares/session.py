from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.db_connector import DatabaseConnector


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, db: DatabaseConnector):
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.db.session_factory.begin() as db_session:
            data["db_session"] = db_session
            return await handler(event, data)
