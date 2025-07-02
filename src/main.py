
import asyncio
from logger import *
from config import config
from http_server import HttpServer
from handlers.start import start_router
from handlers.web_app import app_router
from bot import *

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("Main")


async def send_messages():
    while not messages_queue.empty():
        message_pack = messages_queue.get()
        await message_pack()


async def main():
    try:
        httpd = HttpServer(port = config["server"]["port"])

        scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        scheduler.add_job(send_messages, 'interval', seconds=3)
        scheduler.start()

        dispatcher = Dispatcher(storage = MemoryStorage())
        dispatcher.include_router(start_router)
        dispatcher.include_router(app_router)

        await bot.delete_webhook(drop_pending_updates = True, request_timeout = 10)
        await dispatcher.start_polling(bot)

    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        httpd.join()
        pass

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
