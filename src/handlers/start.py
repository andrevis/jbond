from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from logger import *

start_router = Router()

logger = logging.getLogger("Start")

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f'CommandStart {message.from_user.full_name}')
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')

@start_router.message(Command('start_2'))
async def cmd_start_2(message: Message):
    logger.info(f'start_2 {message.from_user.full_name}')
    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()')

@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    logger.info(f'start_3 {message.from_user.full_name}')
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')