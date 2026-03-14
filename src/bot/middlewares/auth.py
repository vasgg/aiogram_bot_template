from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.user import add_user_to_db, get_user_from_db_by_tg_id


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        from_user = event.from_user
        if from_user is None:
            return await handler(event, data)

        db_session = cast(AsyncSession, data["db_session"])
        user = await get_user_from_db_by_tg_id(from_user.id, db_session)
        if user is None:
            user = await add_user_to_db(from_user, db_session)

        data["user"] = user
        return await handler(event, data)
