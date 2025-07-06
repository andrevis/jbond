import queue
from datetime import datetime
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from bot import bot
from logger import *
from bonds.defaults import DefaultsGetter

logger = logging.getLogger("Messages")

messages_queue = queue.Queue()
pending_messages = queue.Queue()

async def send_message_pack():
    while not messages_queue.empty():
        message_pack = messages_queue.get()
        await message_pack()


class SendMessageTask(object):
    def __init__(self, chat_id, paper):
        self.chat_id = chat_id
        self.paper = paper

    def get_int(self, key):
        value = self.paper[key]
        return int(0 if not value else value)

    def get_float(self, key):
        value = self.paper[key]
        return float(0.0 if not value else value)

    def get_defaults(self, isin):
        defaults = DefaultsGetter.get(isin)
        if defaults == None:
            return "неизвестно"
        elif len(defaults) == 0:
            return "не было"
        else:
            return ', '.join(defaults)

    async def __call__(self, last: bool):
        logger.info(f'Send message to {self.chat_id}')
        try:
            isin            = self.paper["ISIN"]
            name            = self.paper["SHORTNAME"]
            nominal         = self.get_float("FACEVALUE")
            redemption      = self.get_int("DAYSTOREDEMPTION")
            duration        = self.get_int("DURATION")
            coupon          = self.get_float("COUPONPERCENT")
            yieldatwap      = self.get_float("YIELDATWAP")
            couponlength    = self.get_int("COUPONLENGTH")
            price_percent   = self.get_float("PRICE")
            price_rub       = self.get_float("PRICE_RUB")
            qual            = "да" if self.get_int("IS_QUALIFIED_INVESTORS") == 0 else "нет"
            offer           = self.paper['OFFERDATE'] if self.paper['OFFERDATE'] else "нет"
            defaults        = self.get_defaults(isin)
            matdate         = self.paper["MATDATE"]

            text = f'''📌 Имя:\t<b>{name}</b>
🔎 ISIN:\t<b><a href="https://www.moex.com/ru/issue.aspx?code={isin}">{isin}</a></b>
💲 Цена:\t<b>{price_percent}%</b> ({price_rub}₽ / {nominal}₽)
📈 Доходность:\t<b>{yieldatwap}%</b>
📆 Купон:\t<b>{coupon}%</b> (раз в {round(couponlength/30)} мес.)
⏳ Погашение:\t<b>{matdate}</b> ({redemption} д.)
🐹 Доступно для неквалов:\t<b>{qual}</b>
📞 Оферта:\t<b>{offer}</b>
❌ Дефолты:\t<b>{defaults}</b>
⏰ Дюрация:\t<b>{round(duration/30, 1)} мес</b> ({duration} дней)'''

            if last:
                builder = InlineKeyboardBuilder()
                builder.add(InlineKeyboardButton(text="Показать еще", callback_data="more"))
                await bot.send_message(chat_id=self.chat_id, text=text, disable_notification=True, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=builder.as_markup())
            else:
                await bot.send_message(chat_id=self.chat_id, text=text, disable_notification=True, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception as e:
            logger.error(f'Cannot send bot message len={len(text)}: {e}\n{text}')



class MessagePack:
    shift = 5

    def __init__(self, chat_id, sortby):
        self.messages = []
        self.chat_id = chat_id
        self.sortby = sortby
        self.offset = 0
        self.idx = 0

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self.messages[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration  # Done iterating.

    def append(self, message: SendMessageTask):
        self.messages.append(message)

    def __len__(self):
        return len(self.messages)

    def __pending__(self):
        while not pending_messages.empty():
            pending_messages.get()

        pending = MessagePack(self.chat_id, self.sortby)
        pending.messages = self.messages[self.shift:]
        pending.offset = self.offset + self.shift
        pending_messages.put(pending)

    async def __call__(self):
        formatted_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if self.offset == 0:
            await bot.send_message(chat_id=self.chat_id, text=f'=== {formatted_datetime} ({self.shift} из {len(self.messages)})')

        for i, job in enumerate(self.messages):
            if i == self.shift:
                self.__pending__()
                return
            await job(i == self.shift - 1)
