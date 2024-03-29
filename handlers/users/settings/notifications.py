from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import inline
from keyboards.inline import notification, notify_time, back_callback, day, events
from keyboards.inline.settings import get_keyboard
from loader import dp
from models import User, Chat, Notification
from models.event import Day, Event
from states import settings, menu
from states.settings.chat_settings import ChatSettingsStates
from states.settings.edit_notifications import EditNotificationsStates
from utils.misc import get_current_user
from middlewares import _


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='settings'), state=settings.SettingsStates.notifications)
async def back_to_settings(callback: types.CallbackQuery, user: User, state: FSMContext):
    await callback.answer(_("Ты вернулся назад"))
    data = await state.get_data()
    if data.get('chat_id'):
        chat = await Chat.filter(id=int(data.get('chat_id'))).first()
        keyboard = await inline.settings.get_keyboard(False)
        await callback.message.edit_text(_("Настройки чата - {}".format(chat.title)),
                                         reply_markup=keyboard)
        await ChatSettingsStates.chat.set()
        return
    keyboard = await get_keyboard(True)
    await callback.message.edit_text(_("Настройки:"), reply_markup=keyboard)
    await menu.MenuStates.settings.set()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='cancel'), state=settings.SettingsStates.notifications)
async def notifications_actions(callback: types.CallbackQuery, user: User, state: FSMContext):
    await callback.answer(_("Ты вернулся назад"))
    keyboard = await notification.get_keyboard(user)
    data = await state.get_data()
    if data.get('chat_id'):
        chat = await Chat.filter(id=int(data.get('chat_id'))).first()
        keyboard = await notification.get_keyboard(chat, True)
    await callback.message.edit_text(_('Уведомления:'), reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(state=settings.SettingsStates.notifications)
async def notifications_actions(callback: types.CallbackQuery, user: User, state: FSMContext):
    if callback.data == 'notification-trigger':
        await callback.answer("")
        data = await state.get_data()
        if data.get('chat_id'):
            chat = await Chat.filter(id=int(data.get('chat_id'))).first()
            chat.notification = not chat.notification
            await chat.save()
            keyboard = await notification.get_keyboard(chat, True)
            await callback.message.edit_reply_markup(keyboard)
            return
        user.notification = not user.notification
        await user.save()
        keyboard = await notification.get_keyboard(user)
        await callback.message.edit_reply_markup(keyboard)
    elif callback.data == 'time-notification':
        await callback.answer("")
        await callback.message.edit_text(_("За сколько минут до события ты хочешь получать от меня напоминание?"),
                                         reply_markup=notify_time.keyboard)
    elif callback.data.startswith('notify-'):
        await callback.answer(
            _('Ок, буду напоминать тебе за {} минут до начала события!'.format(callback.data.split('-')[-1])))
        data = await state.get_data()
        if data.get('chat_id'):
            chat = await Chat.filter(id=int(data.get('chat_id'))).first()
            chat.notification_time = callback.data.split('-')[-1]
            await chat.save()
            keyboard = await notification.get_keyboard(chat, True)
            await callback.message.edit_text(_('Уведомления:'), reply_markup=keyboard)
            return
        user.notification_time = callback.data.split('-')[-1]
        await user.save()
        keyboard = await notification.get_keyboard(user)
        await callback.message.edit_text(_('Уведомления:'), reply_markup=keyboard)
    elif callback.data == 'notifications':
        await callback.answer()
        await callback.message.edit_text(_('Выбери день недели:'), reply_markup=day.keyboard)
        await EditNotificationsStates.day.set()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=EditNotificationsStates.day)
async def back_to_notification(callback: types.CallbackQuery, user: User):
    await callback.answer(_("Ты вернулся назад"))
    keyboard = await notification.get_keyboard(user)
    await callback.message.edit_text(_('Уведомления:'), reply_markup=keyboard)
    await settings.SettingsStates.notifications.set()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='subgroup'), state=EditNotificationsStates.event)
async def back_to_notification(callback: types.CallbackQuery, user: User):
    await callback.answer(_("Ты вернулся назад"))
    await callback.message.edit_text(_('Выбери день недели:'), reply_markup=day.keyboard)
    await EditNotificationsStates.day.set()


@get_current_user()
@dp.callback_query_handler(state=EditNotificationsStates.day)
async def choose_day(callback: types.CallbackQuery, user: User, state: FSMContext):
    await callback.answer("")
    if callback.data in [day.value for day in Day]:
        await state.update_data(day=callback.data)
        await user.fetch_related("subgroups")
        keyboard = await events.get_keyboard(callback.data, user.group_id, False, list(user.subgroups), True, user)
        await callback.message.edit_text(_('Выбери событие:'), reply_markup=keyboard)
        await EditNotificationsStates.event.set()


@get_current_user()
@dp.callback_query_handler(state=EditNotificationsStates.event)
async def add_or_delete_notification(callback: types.CallbackQuery, user: User, state: FSMContext):
    if callback.data.startswith('event-'):
        notification = await Notification.filter(user=user.id, event=int(callback.data.split('-')[-1])).first()
        if notification:
            await callback.answer(_("Напоминание удалено"))
            await notification.delete()
        else:
            await callback.answer(_("Напоминание создано"))
            event = await Event.filter(id=int(callback.data.split('-')[-1])).first()
            await Notification.create(event=event, user=user)
        await user.fetch_related("subgroups")
        data = await state.get_data()
        keyboard = await events.get_keyboard(data.get('day'), user.group_id, False, list(user.subgroups), True, user)
        await callback.message.edit_text(_('Выбери событие:'), reply_markup=keyboard)
        await EditNotificationsStates.event.set()
