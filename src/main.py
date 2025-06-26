
import asyncio
from logger import *
from config import config
from http_server import HttpServer
from handlers.start import start_router
from handlers.web_app import app_router

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

logger = logging.getLogger("Main")


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    bot = Bot(token = config['bot']['token'])

    dispatcher = Dispatcher(storage = MemoryStorage())
    dispatcher.include_router(start_router)
    dispatcher.include_router(app_router)

    await bot.delete_webhook(drop_pending_updates = True, request_timeout = 10)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    httpd = HttpServer(config["server"]["port"])
    httpd.start()
    asyncio.run(main())
    httpd.join()