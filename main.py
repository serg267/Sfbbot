from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN, ADMINCHAT, START_BOT, STOP_BOT
from aiogram.filters import Command
from aiogram import F
import asyncio
import logging


from core.handlers.basic import command_start, forward_media_to_admin_chat, \
    answer_to_user, command_help, forward_msg_to_admin_chat
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

    bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.message.middleware.register(AlbumMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(command_start, Command(commands=['start']))
    dp.message.register(command_help, Command(commands=['help']))
    dp.message.register(answer_to_user,
                        F.chat.id == int(ADMINCHAT),
                        F.text | F.photo | F.audio | F.video | F.document | F.voice)

    dp.message.register(forward_msg_to_admin_chat,
                        F.chat.id != int(ADMINCHAT),
                        F.media_group_id.func(lambda media_group_id: media_group_id is None),
                        F.text | F.photo | F.audio | F.video | F.document | F.voice)

    dp.message.register(forward_media_to_admin_chat,
                        F.chat.id != int(ADMINCHAT),
                        ~F.media_group_id.func(lambda media_group_id: media_group_id is None),
                        F.text | F.photo | F.audio | F.video | F.document | F.voice)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
