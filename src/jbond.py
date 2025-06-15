# import signal
import os
# import sys
from logger import *

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

with open("/opt/jbond/token", 'r') as token:
    bot = Bot(token=token.readline().strip())
dispatcher = Dispatcher(storage=MemoryStorage())
