
import asyncio
from logger import *
from config import config
from http_server import HttpServer
from handlers import base_router
from bot import *
from messages import *

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("Main")

async def main():
    try:
        httpd = HttpServer(port = config["server"]["port"])

        scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        scheduler.add_job(send_message_pack, 'interval', seconds=3)
        scheduler.start()

        dispatcher = Dispatcher(storage = MemoryStorage())
        dispatcher.include_router(base_router)

        await bot.delete_webhook(drop_pending_updates = True, request_timeout = 10)
        await dispatcher.start_polling(bot)

    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        httpd.join()
        pass

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
