# import signal
import os
# import sys
from logger import *

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# def signal_handler(sig, frame):
#     raise RuntimeError('Interrupted Ctrl+C')

# signal.signal(signal.SIGINT, signal_handler)


#with open("/opt/jbond/token", 'r') as token:
bot = Bot(token=os.environ.get('JBOND_BOT_TOKEN'))
dispatcher = Dispatcher(storage=MemoryStorage())


# async def main():
#     await dispatcher.start_polling(bot)

# def main():
#     timer = TimeThread()
#     timer.start()

#     jbond = JBond()
#     jbond.start()

#     while (True):
#         sleep(1)

# if __name__ == '__main__':
#     main()
