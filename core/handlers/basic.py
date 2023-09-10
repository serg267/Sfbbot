import json
from typing import Dict

from aiogram import Bot, types
from aiogram.types import Message, InputMediaPhoto, MessageEntity
from config import ADMINCHAT, SAY_HELLO, SAY_HELP
import logging

from core.models.models import LinkedMessage


async def command_start(message: Message, bot: Bot) -> None:
    """Command /start handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}! {SAY_HELP}')


async def command_help(message: Message, bot: Bot) -> None:
    """Command /help handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}! {SAY_HELP}')


async def forward_msg_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will forward a message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)
    # json_str = json.dumps(message.__dict__, default=str, indent=True)
    # print(json_str)
    msg = await bot.forward_message(chat_id=ADMINCHAT, from_chat_id=message.from_user.id, message_id=message.message_id)

    linked_msg = LinkedMessage(msg.message_id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)


async def forward_media_to_admin_chat(message: Message, bot: Bot, album: list[types.Message]) -> None:
    """This handler will forward a complete album of any type."""

    if not album:
        album = [message]

    media = []
    for obj in album:
        new_message = obj.caption
        if obj.caption_entities:

            for entity in obj.caption_entities:
                tags = {'bold': 'b',
                        'italic': 'i',
                        'underline': 'u',
                        'strikethrough': 's',
                        'spoiler': 'tg-spoiler',
                        'code': 'code',
                        'pre': 'pre',
                        'text_link': None}
                if entity.type not in tags.keys():
                    continue
                #  right way to extract entity instead of obj.caption[entity.offset:entity.offset + entity.length:]
                pattern = entity.extract_from(obj.caption)
                shift_offset = new_message.index(pattern, int(entity.offset))

                if entity.type == 'text_link':
                    new_pattern = f'<a href="{entity.url}">{pattern}</a>'
                else:
                    new_pattern = f'<{tags.get(entity.type)}>{pattern}</{tags.get(entity.type)}>'

                before = new_message[:shift_offset]
                after = new_message[shift_offset + len(pattern):]  # shift + pattern length
                new_message = f'{before}{new_pattern}{after}'

        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id
        try:
            photo = InputMediaPhoto(types='photo',
                                    media=file_id,
                                    caption=new_message)
            media.append(photo)
        except ValueError:
            await message.answer("This type of album is not supported by bot.")

    msgs = await bot.send_media_group(chat_id=ADMINCHAT, media=media)
    linked_msg = LinkedMessage(msgs[0].message_id)
    linked_msg.set_first_msg(message)


async def answer_to_user(message: Message, bot: Bot) -> None:
    """This handler will forward reply to user from admin chat """
    linked_msg = LinkedMessage.get_element(message.reply_to_message.message_id)
    chat_id = linked_msg.first_message_chat_id
    msg_id = linked_msg.first_message_id

    try:
        json_str = json.dumps(message.__dict__, default=str)
        print(json_str)
        logging.debug(f'answer_to_user {chat_id}')
        await bot.send_message(chat_id=chat_id, text=message.text, reply_to_message_id=msg_id)
    except Exception as error:
        logging.error(error, exc_info=True)
