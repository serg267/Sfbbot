import json

from aiogram import Bot, Router
from aiogram.filters import and_f
from aiogram.types import Message
from aiogram import F

from config import ADMINCHAT, EMO1
from core.models.models import LinkedMessage


def get_replied_message_id(message: Message) -> int or None:
    """if it is replied message gets id and chat id of original"""
    if message.reply_to_message:
        return LinkedMessage.get_element(message.reply_to_message.message_id,
                                         message.reply_to_message.chat.id).first_message_id
    return None


async def resend_msg_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend a text message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)
    # json_str = json.dumps(message.__dict__, default=str, indent=True)
    # print(json_str)

    text = message.text or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_message(chat_id=ADMINCHAT,
                                 text=text_with_username,
                                 entities=message.entities,
                                 reply_to_message_id=get_replied_message_id(message),
                                 allow_sending_without_reply=True
                                 )

    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)
    #
    # json_str = json.dumps(msg.__dict__, default=str)
    # print(json_str)


async def resend_photo_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend a photo message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    text = message.caption or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_photo(chat_id=ADMINCHAT,
                               photo=message.photo[-1].file_id,
                               caption=text_with_username,
                               caption_entities=message.caption_entities,
                               reply_to_message_id=get_replied_message_id(message),
                               allow_sending_without_reply=True
                               )
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)


async def resend_video_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend a video message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    text = message.caption or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_video(chat_id=ADMINCHAT,
                               video=message.video.file_id,
                               duration=message.video.duration,
                               width=message.video.width,
                               height=message.video.height,
                               caption=text_with_username,
                               caption_entities=message.caption_entities,
                               reply_to_message_id=get_replied_message_id(message),
                               allow_sending_without_reply=True
                               )
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)


async def resend_audio_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend an audio message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    text = message.caption or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_audio(chat_id=ADMINCHAT,
                               audio=message.audio.file_id,
                               duration=message.audio.duration,
                               performer=message.audio.performer,
                               title=message.audio.title,
                               caption=text_with_username,
                               caption_entities=message.caption_entities,
                               reply_to_message_id=get_replied_message_id(message),
                               allow_sending_without_reply=True
                               )
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)


async def resend_voice_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend a voice message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    text = message.caption or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_voice(chat_id=ADMINCHAT,
                               voice=message.voice.file_id,
                               duration=message.voice.duration,
                               caption=text_with_username,
                               caption_entities=message.caption_entities,
                               reply_to_message_id=get_replied_message_id(message),
                               allow_sending_without_reply=True
                               )
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)


async def resend_document_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend a document message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    text = message.caption or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_document(chat_id=ADMINCHAT,
                                  document=message.document.file_id,
                                  thumbnail=message.document.thumbnail.file_id,
                                  caption=text_with_username,
                                  caption_entities=message.caption_entities,
                                  reply_to_message_id=get_replied_message_id(message),
                                  allow_sending_without_reply=True
                                  )
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)
    print(msg.content_type)


async def resend_animation_to_admin_chat(message: Message, bot: Bot) -> None:
    """This handler will resend an animation message to admin chat"""
    json_str = json.dumps(message.__dict__, default=str)
    print(json_str)

    text = message.caption or ''
    text_with_username = f"{text}\n{EMO1} {message.chat.first_name} (@{message.chat.username})"
    msg = await bot.send_animation(chat_id=ADMINCHAT,
                                   animation=message.animation.file_id,
                                   duration=message.animation.duration,
                                   width=message.animation.width,
                                   height=message.animation.height,
                                   caption=text_with_username,
                                   caption_entities=message.caption_entities,
                                   reply_to_message_id=get_replied_message_id(message),
                                   allow_sending_without_reply=True)
    linked_msg = LinkedMessage(msg.message_id, msg.chat.id)
    linked_msg.set_first_msg(message)

    json_str = json.dumps(msg.__dict__, default=str)
    print(json_str)
    print(msg.content_type)

# create router instance
resend_msg_router = Router()
# common filters
resend_msg_router.message.filter(F.chat.id != int(ADMINCHAT),
                                 and_f(~F.forward_from, ~F.forward_from_chat),
                                 ~F.media_group_id)
# register filtered message handlers
resend_msg_router.message.register(resend_msg_to_admin_chat, F.text)
resend_msg_router.message.register(resend_photo_to_admin_chat, F.photo)
resend_msg_router.message.register(resend_video_to_admin_chat, F.video)
resend_msg_router.message.register(resend_audio_to_admin_chat, F.audio)
resend_msg_router.message.register(resend_voice_to_admin_chat, F.voice)
resend_msg_router.message.register(resend_document_to_admin_chat, F.document)
resend_msg_router.message.register(resend_animation_to_admin_chat, F.animation)
