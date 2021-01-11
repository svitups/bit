from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram import types
from models.user import User


class CurrentUserMiddleware(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):
        handler = current_handler.get()
        if handler and getattr(handler, 'get_current_user', False):
            user = await User().select_user_by_tele_id(msg.from_user.id)
            if user:
                data['user'] = user
            else:
                await msg.answer("""
Похоже, что вас не в базе данных.
Чтобы это исправить - нажмите на /enter            
                """)
                raise CancelHandler()

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        handler = current_handler.get()
        if handler and getattr(handler, 'get_current_user', False):
            user = await User().select_user_by_tele_id(msg.from_user.id)
            if user:
                data['user'] = user
            else:
                await msg.answer("""
Похоже, что вас не в базе данных.
Чтобы это исправить - нажмите на /enter            
                """)
                raise CancelHandler()