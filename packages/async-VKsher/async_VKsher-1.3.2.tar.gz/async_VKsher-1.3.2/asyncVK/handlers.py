from typing import Union
import traceback
import sys

import asyncio
import aiohttp

from .dispatcher import Dispatcher, get_dispatcher_by_event
from .condition import Condition, And, Or
from .core import get_event_params


class Handler:
    event_type = None

    def __init__(self, condition: Union[Condition, And, Or], is_lower: bool = False, func=None):
        self.condition = condition
        self.is_lower = is_lower
        self.func = func

    def __call__(self, func):
        async def wrapper(token: str, event: dict, event_type: str):
            await func(get_dispatcher_by_event(token, event, event_type))

        return type(self)(self.condition, self.is_lower, wrapper)

    async def new_event(self, token: str, event: dict) -> None:
        event_params = get_event_params(event, self.event_type, self.is_lower)
        if self.condition.new_event(event_params):
            try:
                await self.func(token, event, self.event_type)
            except:
                sys.stderr.write(f"\n\n{traceback.format_exc()}\n\n")


class CustomHandler(Handler):
    def __call__(self, func):
        async def wrapper(token: str, event: dict, event_type: str):
            await func(get_dispatcher_by_event(token, event, event_type))

        handler = CustomHandler(self.condition, self.is_lower, wrapper)
        handler.event_type = self.event_type
        return handler


class MessageNewHandler(Handler):
    event_type = "message_new"


class MessageEditHandler(Handler):
    event_type = "message_edit"


class WallReplyNewHandler(Handler):
    event_type = "wall_reply_new"


class WallReplyEditHandler(WallReplyNewHandler):
    event_type = "wall_reply_edit"


class WallPostNewHandler(Handler):
    event_type = "wall_post_new"


class BoardPostNewHandler(Handler):
    event_type = "board_post_new"


class BoardPostEditHandler(BoardPostNewHandler):
    event_type = "board_post_edit"


class Handlers:
    message_new = MessageNewHandler
    message_edit = MessageEditHandler
    wall_reply_new = WallReplyNewHandler
    wall_reply_edit = WallReplyEditHandler
    wall_post_new = WallPostNewHandler
    board_post_new = BoardPostNewHandler
    board_post_edit = BoardPostEditHandler

    def __new__(cls, event_type):
        handler = CustomHandler()
        handler.event_type = event_type
        return handler
