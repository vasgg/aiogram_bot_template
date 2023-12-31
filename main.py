import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings
from core.middlewares.auth_middleware import AuthMiddleware
from core.middlewares.session_middleware import SessionMiddleware
from core.middlewares.updates_dumper_middleware import UpdatesDumperMiddleware
from core.resources.notify_admin import on_shutdown_notify, on_startup_notify
from core.handlers.base_handlers import router as base_router
from core.handlers.errors_handler import router as errors_router


async def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode='HTML')
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)
    dispatcher.message.middleware(SessionMiddleware())
    dispatcher.callback_query.middleware(SessionMiddleware())
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(on_startup_notify)
    dispatcher.shutdown.register(on_shutdown_notify)
    dispatcher.include_routers(base_router, errors_router)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
