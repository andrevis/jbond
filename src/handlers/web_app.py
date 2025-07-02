from aiogram import Router
from aiogram.types import Message
from logger import *

app_router = Router()

logger = logging.getLogger("App")

@app_router.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: Message):
    logger.info(f'{message.web_app_data}')
    await message.answer(f'{message.web_app_data}')
