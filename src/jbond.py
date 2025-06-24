# import signal
import os
# import sys
from logger import *
from environment import *

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = open('/opt/jbond/token', 'r').readline().strip()

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(storage=MemoryStorage())
