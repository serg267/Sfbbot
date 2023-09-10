import json
from aiogram import Bot, types
from aiogram.types import Message, InputMediaPhoto, MessageEntity
from config import ADMINCHAT, SAY_HELLO, SAY_HELP
import logging


async def command_start(message: Message, bot: Bot) -> None:
    """Command /start handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}! {SAY_HELP}')


async def command_help(message: Message, bot: Bot) -> None:
    """Command /help handler"""
    await bot.send_message(message.from_user.id, f'{SAY_HELLO}{message.from_user.first_name}! {SAY_HELP}')


async def forward_msg_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will forward a message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str, indent=True)
    print(json_str)
    await bot.forward_message(chat_id=ADMINCHAT, from_chat_id=message.from_user.id, message_id=message.message_id)


async def forward_media_to_admin_chat(message: Message, bot: Bot, album: list[types.Message]) -> None:
    """This handler will forward a complete album of any type."""
    # json_str = json.dumps(message.__dict__, default=str)
    # print(json_str)

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

    await bot.send_media_group(chat_id=ADMINCHAT, media=media)


async def answer_to_user(message: Message, bot: Bot) -> None:
    """This handler will forward reply to user from admin chat """
    # user_id = message.reply_to_message.forward_from.id or None # forward message to author of the fist message
    user_id = message.from_user.id or None
    try:
        await bot.send_message(user_id, message.text)
    except Exception as error:
        logging.error(error, exc_info=True)
