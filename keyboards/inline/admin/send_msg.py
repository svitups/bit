from aiogram import types
from models import Admin, User
from keyboards.inline import blank_callback, back_callback
from middlewares import _


async def get_keyboard(admin: Admin):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if admin:
        keyboard.add(types.InlineKeyboardButton(_("Все отправленные сообщения"), callback_data='all-msgs'))
        if admin.role.name == 'supreme':
            keyboard.add(types.InlineKeyboardButton(_('Отправить всем'), callback_data='send-all'))
        elif admin.role.name == 'improved':
            keyboard.add(types.InlineKeyboardButton(_('Отправить всему факультету'), callback_data='send-faculty'))
        else:
            keyboard.add(types.InlineKeyboardButton(_('Отправить группе'), callback_data='send-group'))
    else:
        keyboard.add(types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='settings')))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
    return keyboard