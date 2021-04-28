from aiogram import types
from keyboards.inline import back_callback, create_callback
from middlewares import _


async def get_keyboard(category):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(_('Сохранить'), callback_data=create_callback.new(category=category)))
    keyboard.add(types.InlineKeyboardButton(_('Отмена'), callback_data=back_callback.new(category='cancel')))
    return keyboard