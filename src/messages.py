import queue
from datetime import datetime
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from bot import bot
from logger import *
from bonds.defaults import DefaultsGetter
from bonds.rating import RatingGetter

logger = logging.getLogger("Messages")

ratings = ['BB-','BB','BB+','BBB-','BBB','BBB+','A-','A','A+','AA-','AA','AA+','AAA-','AAA']

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
            name            = self.paper["NAME"]
            shortname       = self.paper["SHORTNAME"]
            nominal         = self.get_float("FACEVALUE")
            redemption      = self.get_int("DAYSTOREDEMPTION")
            duration        = self.get_int("DURATION")
            coupon          = self.get_float("COUPONPERCENT")
            yieldatwap      = self.get_float("YIELDATWAP")
            couponlength    = self.get_int("COUPONLENGTH")
            price           = self.get_float("WAPRICE")
            qual            = "да" if self.get_int("IS_QUALIFIED_INVESTORS") == 0 else "нет"
            offer           = self.paper['OFFERDATE'] if self.paper['OFFERDATE'] else "нет"
            defaults        = self.get_defaults(isin)
            matdate         = self.paper["MATDATE"]
            listlevel       = self.paper['LISTLEVEL']
            price_rub       = nominal * price / 100.0
            rating          = self.paper['RATING']

            text = f'''📌 <b>{name}</b>
🔎 ISIN:\t<b><code>{isin}</code>|<a href="https://www.moex.com/ru/issue.aspx?code={isin}">Moex</a>|<a href="https://www.tbank.ru/invest/bonds/{isin}">T-Broker</a></b>
🆎 Рейтинг:\t<b>{rating}</b>, Листинг: {listlevel}
💲 Цена:\t<b>{price:.2f}%</b> ({price_rub:.1f}₽ / {nominal}₽)
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

    def __init__(self, filters):
        self.filters = filters
        self.messages = []
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

        pending = MessagePack(self.filters)
        pending.messages = self.messages[self.shift:]
        pending.offset = self.offset + self.shift
        pending_messages.put(pending)

    async def __call__(self):
        formatted_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if self.offset == 0:
            await bot.send_message(chat_id= self.filters.chat_id, text=f'=== {formatted_datetime} ({self.shift} из {len(self.messages)})')

        done = 0
        total = 0
        while done < self.shift and total < len(self.messages):
            messages = self.messages[total:]

            batch = min(self.shift, len(messages))
            rating_tasks = [asyncio.to_thread(RatingGetter.get, job.paper['ISIN']) for job in messages[:batch]]
            results = await asyncio.gather(*rating_tasks)

            for i, result in enumerate(results):
                total += 1             

                if result == None:
                    continue

                job = messages[i]
                job.paper['RATING'] = results[i]

                if ratings.index(job.paper['RATING']) < ratings.index(self.filters.rating):
                    continue

                done += 1
                is_last = (done == self.shift) or (total == len(self.messages))
                await job(is_last)

                if is_last:
                    self.__pending__()
                    return


