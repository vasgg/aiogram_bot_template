import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import TelegramObject


class UpdatesDumperMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        json_event = event.model_dump_json(exclude_unset=True)

        logging.info(json_event)
        res = await handler(event, data)
        if res is UNHANDLED:
            logging.info("UNHANDLED")
        return res
