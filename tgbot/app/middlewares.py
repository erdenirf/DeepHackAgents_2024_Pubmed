from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Awaitable, Dict

# class WebHook(BaseMiddleware):
#     async def on_process_message(self, message: Message, data: Dict[str, Any], *args, **kwargs) -> Any:
#         if message.text == "ping":
#             await message.answer("pong")
#         return message