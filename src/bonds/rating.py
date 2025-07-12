import requests
from bs4 import BeautifulSoup
from logger import *
from lxml import etree

logger = logging.getLogger("Rating")


class RatingGetter:

    @staticmethod
    def get(isin):
        try:
            url = f'https://analytics.dohod.ru/bond/{isin}'

            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                logger.error(f'Cannot get rating (code={response.status_code}): {response.reason}')
                return None

            root = BeautifulSoup(response.content, 'html.parser')
            dom = etree.HTML(str(root))
            return dom.xpath('//*[@id="liquidityScroll"]/div[3]/div[2]/div/div[2]/p/span/span[1]/span')[0].text
        except ValueError as e:
            logger.error(f'Cannot get rating: {e}')
            return None



