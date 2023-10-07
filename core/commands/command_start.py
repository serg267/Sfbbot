from aiogram import Bot
from aiogram.types import Message

from config import SAY_HELLO, SAY_HELP


async def command_start(message: Message, bot: Bot) -> None:
    """Command /start handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}! {SAY_HELP}')