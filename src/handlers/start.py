from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import config
from logger import *

start_router = Router()

logger = logging.getLogger("Start")

@start_router.message(CommandStart())
async def handle_start(message: Message):
    logger.info(f'Command /start from {message.from_user.full_name}')
    address = config["server"]["address"]
    port = config["server"]["port"]
    webAppInfo = WebAppInfo(url = f"https://{address}:{port}")
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = 'Открыть фильтры', web_app = webAppInfo))
    await message.answer(text = f'Поехали', reply_markup = builder.as_markup())

@start_router.message(Command('filters'))
async def cmd_filters(message: Message):
    logger.info(f'Command /filters from {message.from_user.full_name}')
    address = config["server"]["address"]
    port = config["server"]["port"]
    webAppInfo = WebAppInfo(url = f"https://{address}:{port}")
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = 'Открыть фильтры', web_app = webAppInfo))
    await message.answer(text = 'Хуильтры', reply_markup = builder.as_markup())
