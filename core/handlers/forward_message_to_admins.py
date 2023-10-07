import json

from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.types import Message

from config import ADMINCHAT
from core.models.models import LinkedMessage


async def forward_msg_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will forward message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    msg = await bot.forward_message(chat_id=ADMINCHAT,
                                    from_chat_id=message.from_user.id,
                                    message_id=message.message_id,
                                    )
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)

# create router instance
forward_msg_router = Router()
# register filtered message handler
forward_msg_router.message.register(forward_msg_to_admin_chat,
                                    F.chat.id != int(ADMINCHAT),
                                    or_f(F.forward_from, F.forward_from_chat),
                                    ~F.media_group_id)
