from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.misc import logging

from data import config

bot = Bot(config.API_TOKEN, validate_token=True)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = None
scheduler = AsyncIOScheduler()

logging.setup()
