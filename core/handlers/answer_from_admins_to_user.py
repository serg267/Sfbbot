import json
import logging

from aiogram import Bot, Router, F
from aiogram.types import Message

from config import ADMINCHAT
from core.models.models import LinkedMessage


async def answer_to_user(message: Message, bot: Bot) -> None:
    """This handler will forward reply to user from admin chat """
    linked_msg = LinkedMessage.get_element(message.reply_to_message.message_id, message.reply_to_message.chat.id)
    msg_id = linked_msg.first_message_id
    chat_id = linked_msg.first_message_chat_id

    try:
        json_str = json.dumps(message.__dict__, default=str)
        print(json_str)
        logging.debug(f'answer_to_user {chat_id}')
        msg = await bot.send_message(chat_id=chat_id, text=message.text, reply_to_message_id=msg_id)
        linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
        linked_msg.set_first_msg(message)
        json_str = json.dumps(msg.__dict__, default=str)
        print(json_str)
    except Exception as error:
        logging.error(error, exc_info=True)


answer_to_user_router = Router()
answer_to_user_router.message.register(answer_to_user,
                                       F.chat.id == int(ADMINCHAT),
                                       F.text | F.photo | F.audio | F.video | F.document | F.voice)
