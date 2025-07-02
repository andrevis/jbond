
from config import config
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions
from logger import *
import queue


logger = logging.getLogger("Jbond")

bot = Bot(token = config['bot']['token'])

messages_queue = queue.Queue()

class SendMessageTask(object):
    def __init__(self, chat_id, paper):
        self.chat_id = chat_id
        self.paper = paper

    async def __call__(self):
        logger.info(f'Send message to {self.chat_id}')
        try:

            isin = self.paper["ISIN"]
            name = self.paper["NAME"]
            duration = self.paper["DURATION"]
            coupon = self.paper["COUPONPERCENT"]
            coupon_date = self.paper["COUPONDATE"]
            yieldatwap = self.paper["YIELDATWAP"]
            couponlength = self.paper["COUPONLENGTH"]
            price_percent = self.paper["PRICE"]
            price_rub = self.paper["PRICE_RUB"]
            qual = "да" if (int(self.paper["IS_QUALIFIED_INVESTORS"]) == 0) else "нет"


            text = f'''📌 Имя:\t<b>{name}</b>
🔎 ISIN:\t<b><a href="https://www.moex.com/ru/issue.aspx?code={isin}">{isin}</a></b>
💲 Цена:\t<b>{price_percent}%</b> ({price_rub}₽ )
📈 Доходность:\t<b>{yieldatwap}%</b>
📆 Купон:\t<b>{coupon}%</b> (раз в {round(couponlength/30)} мес.), ближайший {coupon_date}
⏳ Дюрация:\t<b>{duration}</b> дней ({round(duration/30, 1)} мес)
🐹 Доступно для неквалов:\t<b>{qual}</b>
📞 Оферта:\t<b>...</b>'''

            await bot.send_message(chat_id=self.chat_id, text=text, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception as e:
            logger.error(f'Cannot send bot message len={len(text)}: {e}\n{text}')



class MessagePack(list):
    async def __call__(self):
        for task in self:
            await task()