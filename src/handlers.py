from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, WebAppInfo, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from config import config
from bot import bot
from logger import *
from messages import *

base_router = Router()

logger = logging.getLogger("Router")

@base_router.message(CommandStart())
async def handle_start(message: Message):
    logger.info(f'Command /start from {message.from_user.full_name}')
    address = config["server"]["address"]
    port = config["server"]["port"]
    webAppInfo = WebAppInfo(url = f"https://{address}:{port}")
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = 'Открыть фильтры', web_app = webAppInfo))
    await message.answer(text = f'Поехали', reply_markup = builder.as_markup())

@base_router.message(Command('filters'))
async def cmd_filters(message: Message):
    logger.info(f'Command /filters from {message.from_user.full_name}')
    address = config["server"]["address"]
    port = config["server"]["port"]
    webAppInfo = WebAppInfo(url = f"https://{address}:{port}")
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = 'Открыть фильтры', web_app = webAppInfo))
    await message.answer(text = 'Хуильтры', reply_markup = builder.as_markup())

@base_router.message(Command('clear'))
async def cmd_clear(message: Message):
    logger.info(f'Command /clear from {message.from_user.full_name}')
    try:
        # Все сообщения, начиная с текущего и до первого (message_id = 0)
        for i in range(message.message_id, 1, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует), 
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            logger.info(f'History has been cleared')
    

@base_router.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: Message):
    logger.info(f'{message.web_app_data}')
    await message.answer(f'{message.web_app_data}')


@base_router.callback_query(F.data == "more")
async def handle_more(callback: CallbackQuery):
    if not pending_messages.empty():
        messages_queue.put(pending_messages.get())
    await callback.answer('Еще 10 облигаций -->')
