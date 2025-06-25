from logger import *
from config import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token = config['bot']['token'])
dispatcher = Dispatcher(storage = MemoryStorage())
