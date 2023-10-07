from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN, ADMINCHAT, START_BOT, STOP_BOT
import asyncio
import logging

from core.commands import register_base_commands_router
from core.db import create_the_engine, url_object, get_session_maker, proceed_schemas

from core.handlers import register_user_handlers_router
from core.middlewares.mediagroup import AlbumMiddleware


async def start_bot(bot: Bot) -> None:
    """Start bot notify """
    await bot.send_message(ADMINCHAT, text=START_BOT)


async def stop_bot(bot: Bot) -> None:
    """Stop bot notify"""
    await bot.send_message(ADMINCHAT, text=STOP_BOT)


async def main() -> None:
    """launch bot"""
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    # middleware register
    dp.message.middleware.register(AlbumMiddleware())
    # bot commands register
    register_base_commands_router(dp)
    # bot handlers register
    register_user_handlers_router(dp)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    async_engine = create_the_engine(url_object())
    print(async_engine)
    session_maker = get_session_maker(async_engine)
    print(session_maker)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
