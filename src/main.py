
import asyncio
from jbond import *
from handlers.start import start_router
from logger import *
from http_server import *
from environment import *

from aiogram.types import FSInputFile

logger = logging.getLogger("Main")


async def main():

    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    dispatcher.include_router(start_router)

    await bot.delete_webhook(drop_pending_updates=True, request_timeout=10)
    # try:
    #     await bot.delete_webhook(drop_pending_updates=True, request_timeout=10)
    #     res = await bot.set_webhook(
    #         url=f'https://185.68.21.112:{PORT}/webhook',
    #         certificate=FSInputFile('/opt/jbond/cert.pem'),
    #         drop_pending_updates=True,
    #         request_timeout=10
    #     )
    #     if not res:
    #         logger.error(f'Cannot set webhook')

    await dispatcher.start_polling(bot)

    # except Exception as e:
    #     logger.error(f'Exception: {e}')
    # finally:
    #     pass


if __name__ == "__main__":
    httpd = HttpServer(PORT)
    httpd.start()
    asyncio.run(main())
    httpd.join()