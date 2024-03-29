from aiogram import Dispatcher

from data import config
from loader import dp
from .debugger import Debugger

from .throttling import ThrottlingMiddleware
from .current_user import CurrentUserMiddleware
from .current_admin import CurrentAdminMiddleware

from middlewares.lang_middleware import ACLMiddleware
from data.config import I18N_DOMAIN, LOCALES_DIR

i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.gettext

if __name__ == 'middlewares':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CurrentUserMiddleware())
    dp.middleware.setup(CurrentAdminMiddleware())
    if config.DEBUG:
        dp.middleware.setup(Debugger())
    dp.middleware.setup(i18n)
