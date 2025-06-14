import asyncio
from jbond import bot, dispatcher #,scheduler
from handlers.start import start_router


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dispatcher.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())