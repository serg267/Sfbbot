import asyncio
import json
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: int | float = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:

        if not event.media_group_id:  # if it's not media group do nothing
            return await handler(event, data)

        try:
            self.album_data[event.media_group_id].append(event)  # all next messages received
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[event.media_group_id] = [event]  # first message received
            await asyncio.sleep(self.latency)

            data["album"] = self.album_data[event.media_group_id]
            del self.album_data[event.media_group_id]  # clean up after taking the album_data

        return await handler(event, data)

