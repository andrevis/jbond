import requests
from logger import *
from bonds.request import BondsRequest
import json
from operator import attrgetter

logger = logging.getLogger("Bond")

class BondsGetter:
    __columns__ = []

    @property
    def columns(self):
        return self.__columns__

    def __needed__(self, filters, paper):
        if paper['OFFERDATE'] and not filters.is_offer:
            return False

        if paper[filters.sort.key] == 0:
            return False

        if float(paper["PRICE"]) > float(filters.price):
            return False
 
        return True

    def __sort__(self, key, order, papers):
        reverse = (order == "desc")
        logger.info(f'Sorting {order} by {key} - reverse={reverse}')
        return sorted(papers, key=lambda paper: paper[key], reverse=reverse)

    def __convert__(self, filters, paper):
        converted = {}
        for i, column in enumerate(self.__columns__):
            converted[column] = paper[i]

        if not converted[filters.sort.key]:
            converted[filters.sort.key] = 0

        return converted

    def __filter__(self, filters, papers):
        filtered = []
        for paper in papers:
            converted = self.__convert__(filters, paper)
            if self.__needed__(filters, converted):
                filtered.append(converted)
        return filtered

    # "rates.cursor": {
    #     "columns": [ "INDEX", "TOTAL", "PAGESIZE" ],
    #     "data": [[ 0, 214, 100 ]]
    # }
    def __get_total__(self, json):
        for i, key in enumerate(json["rates.cursor"]["columns"]):
            if key == 'TOTAL':
                return int(json["rates.cursor"]["data"][0][i])

        raise Exception(f'Cannot get TOTAL from {json}')

    def get(self, filters):
        logger.info(f'BondsGetter:get {filters}')

        total = 1000
        offset = 0

        filtered_papers = []
        while offset < total:
            scroll = min(100, total - offset)
            logger.info(f'Scrolling from {offset} to {total} by {scroll}')

            # https://iss.moex.com/iss/apps/infogrid/emission/rates.json?lang=ru&iss.meta=off&sort_order=dsc&sort_column=YIELDATWAP&start=0&limit=1000&coupon_frequency=4,12&redemption=60,1080&coupon_percent=20,50&columns=SECID,SHORTNAME,ISIN,FACEVALUE,FACEUNIT,MATDATE,COUPONFREQUENCY,COUPONPERCENT,OFFERDATE,DAYSTOREDEMPTION,SECSUBTYPE,YIELDATWAP,COUPONDATE,PRICE_RUB,PRICE,REPLBOND,ISSUEDATE,COUPONLENGTH,TYPENAME,DURATION,IS_QUALIFIED_INVESTORS&sec_type=stock_corporate_bond,stock_exchange_bond&currencyid=rub&high_risk=0
            url = str(BondsRequest().lang().meta(False).sort(filters.sort.order, filters.sort.key).scroll(offset, scroll).period(filters.period).redemption(filters.redemption.fr, filters.redemption.to).coupons(filters.coupons.fr, filters.coupons.to).qual(filters.is_qual).amortization(filters.is_amort).columns().sec_type().currencyid().high_risk(False).listing([1,2]))
            logger.info(f'Request: {url}')

            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                logger.error(f'Cannot get MOEX request (code={response.status_code}): {response.reason}')
                return None

            json = response.json()
            total = self.__get_total__(json)
            offset += min(scroll, total-offset)

            self.__columns__ = json["rates"]["columns"]
            filtered_papers.extend(self.__filter__(filters, json["rates"]["data"]))

        return self.__sort__(filters.sort.key, filters.sort.order, filtered_papers)
