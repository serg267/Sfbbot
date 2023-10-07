__all__ = ['register_user_handlers_router']
from aiogram import Router

from core.handlers.answer_from_admins_to_user import answer_to_user_router
from core.handlers.forward_message_to_admins import forward_msg_router
from core.handlers.resend_media_group_to_admins import media_group_router
from core.handlers.resend_message_to_admins import resend_msg_router


def register_user_handlers_router(router: Router) -> None:
    """forward, resend, and reply handlers router"""
    router.include_router(resend_msg_router)
    router.include_router(forward_msg_router)
    router.include_router(media_group_router)
    router.include_router(answer_to_user_router)
