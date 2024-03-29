from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram import types
from models import User


class CurrentUserMiddleware(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):
        from middlewares import _
        handler = current_handler.get()
        if handler and getattr(handler, 'get_current_user', False):
            user = await User().select_user_by_tele_id(msg.from_user.id)
            if user:
                data['user'] = user
            else:
                await msg.answer(_("""
Похоже, что тебя нет в базе данных.
Чтобы это исправить - нажми на /start       
                """))
                raise CancelHandler()

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        handler = current_handler.get()
        if handler and getattr(handler, 'get_current_user', False):
            from middlewares import _
            user = await User().select_user_by_tele_id(callback.from_user.id)
            if user:
                data['user'] = user
            else:
                await callback.answer(_("""
Похоже, что тебя нет в базе данных.
Чтобы это исправить - нажми на /start      
                """))
                raise CancelHandler()