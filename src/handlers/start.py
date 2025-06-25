from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import config
from logger import *

start_router = Router()

logger = logging.getLogger("Start")

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f'CommandStart {message.from_user.full_name}')

    webAppInfo = WebAppInfo(url = f"https://{config["server"]["address"]}:{config["server"]["port"]}/index.html")
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = 'Открыть фильтры', web_app = webAppInfo))
    await message.answer(reply_markup = builder.as_markup())

# @start_router.message(Command('filters'))
# async def cmd_filters(message: Message):
#     webAppInfo = WebAppInfo(url = f"https://{ADDR}:{PORT}/index.html")
#     builder = ReplyKeyboardBuilder()
#     builder.add(KeyboardButton(text = 'Открыть фильтры', web_app = webAppInfo))
#     await message.answer(reply_markup = builder.as_markup())

# @start_router.message(F.text == '/start_3')
# async def cmd_start_3(message: Message):
#     logger.info(f'start_3 {message.from_user.full_name}')
#     await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')