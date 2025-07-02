import requests
from logger import *
from bonds.request import BondsRequest
import json

logger = logging.getLogger("Bond")

class BondsGetter:
    __columns__ = []

    @property
    def columns(self):
        return self.__columns__

    def __needed__(self, filters, paper):
        for i, column in enumerate(self.__columns__):
            if column == 'IS_QUALIFIED_INVESTORS':
                value = int(paper[i])
                if value == 1 and not filters.is_qual:
                    return False
            elif column == 'HIGH_RISK':
                value = int(paper[i])
                if value == 1:
                    return False

        return True


    def __filter_paper__(self, paper):
        filtered_paper = {}
        for i, column in enumerate(self.__columns__):
            filtered_paper[column] = paper[i]
        return filtered_paper

    def get(self, filters):
        logger.info(f'BondsGetter:get {filters}')

        request = BondsRequest()
        # https://iss.moex.com/iss/apps/infogrid/emission/rates.json?lang=ru&iss.meta=on&sort_order=dsc&sort_column=YIELDATWAP&start=0&limit=100&coupon_frequency=4,6,12&columns=SECID,SHORTNAME,ISIN,FACEVALUE,FACEUNIT,MATDATE,COUPONFREQUENCY,COUPONPERCENT,OFFERDATE,DAYSTOREDEMPTION,SECSUBTYPE,YIELDATWAP,COUPONDATE,PRICE_RUB,PRICE,REPLBOND,ISSUEDATE,COUPONLENGTH,TYPENAME,DURATION,IS_QUALIFIED_INVESTORS,INN&coupon_percent=20,50&duration=90,1080&sec_type=stock_corporate_bond&currencyid=rub
        url = str(request.lang().meta(False).sort().scroll().period(filters.period).columns().coupons(filters.coupons.fr, filters.coupons.to).duration(filters.duration.fr, filters.duration.to).sec_type().currencyid())
        logger.info(f'Request: {url}')

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            logger.error(f'Cannot get MOEX request (code={response.status_code}): {response.reason}')
            return None

        json = response.json()
        # metadata = json["rates"]["metadata"]
        self.__columns__ = json["rates"]["columns"]

        filtered_papers = []
        for paper in json["rates"]["data"]:
            if self.__needed__(filters, paper):
                filtered_papers.append(self.__filter_paper__(paper))
        return filtered_papers
