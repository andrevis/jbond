
import asyncio
from jbond import *
from handlers.start import start_router
from logger import *
from http_server import *
from config import config

logger = logging.getLogger("Main")


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    dispatcher.include_router(start_router)

    await bot.delete_webhook(drop_pending_updates = True, request_timeout = 10)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    httpd = HttpServer(config["server"]["port"])
    httpd.start()
    asyncio.run(main())
    httpd.join()