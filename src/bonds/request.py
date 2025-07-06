# https://iss.moex.com/iss/apps/infogrid/emission/rates.json?
# lang=ru&
# iss.meta=off&
# sort_order=dsc&
# sort_column=YIELDATWAP&
# start=0&limit=100&
# coupon_frequency=4,12&
# redemption=60,1080&
# coupon_percent=20,50&
# columns=SECID,SHORTNAME,ISIN,FACEVALUE,FACEUNIT,MATDATE,COUPONFREQUENCY,COUPONPERCENT,OFFERDATE,DAYSTOREDEMPTION,SECSUBTYPE,YIELDATWAP,COUPONDATE,PRICE_RUB,PRICE,REPLBOND,ISSUEDATE,COUPONLENGTH,TYPENAME,DURATION,IS_QUALIFIED_INVESTORS&
# sec_type=stock_corporate_bond,stock_exchange_bond&
# currencyid=rub&
# high_risk=0


# колонки
# https://iss.moex.com/iss/apps/infogrid/emission/columns.json?lang=ru&iss.meta=off

class BondsRequest:
    __req__ = None
    __columns__ = [
        'SECID',
        'INITIALFACEVALUE',
        'SHORTNAME',
        'ISIN',
        'FACEVALUE',
        'FACEUNIT',
        'MATDATE',
        'COUPONFREQUENCY',
        'COUPONPERCENT',
        'OFFERDATE',
        'DAYSTOREDEMPTION',
        'SECSUBTYPE',
        'YIELDATWAP',
        'COUPONDATE',
        'PRICE_RUB',
        'PRICE',
        'REPLBOND',
        'ISSUEDATE',
        'COUPONLENGTH',
        'TYPENAME',
        'DURATION',
        'IS_QUALIFIED_INVESTORS',
        'LISTLEVEL'
    ]

    @property
    def get_columns(self):
        return self.__columns__

    def __init__(self):
        self.__req__ = 'https://iss.moex.com/iss/apps/infogrid/emission/rates.json?'

    def lang(self):
        self.__req__ += 'lang=ru&'
        return self

    def meta(self, meta = False):
        val = 'on' if meta else 'off'
        self.__req__ += f'iss.meta={val}&'
        return self

    def sort(self, odred = 'asc', col = 'YIELDATWAP'):
        self.__req__ += f'sort_order={odred}&sort_column={col}&'
        return self

    def scroll(self, start = 0, limit = 100):
        self.__req__ += f'start={start}&limit={limit}&'
        return self

    def period(self, values=[]):
        val = ','.join(map(str, values))
        self.__req__ += f'coupon_frequency={val}&'
        return self

    def columns(self, optional = None):
        columns = ','.join(self.__columns__)
        self.__req__ += f'columns={columns}&'
        if optional:
            self.__req__ += f',{optional}'
        return self

    def amortization(self, include=True):
        if not include:
            self.__req__ += f'amortization=0&'
        return self 

    def qual(self, include=True):
        if not include:
            self.__req__ += f'qi=0&'
        return self 

    def coupons(self, fr, to):
        self.__req__ += f'coupon_percent={fr},{to}&'
        return self

    def redemption(self, fr, to):
        self.__req__ += f'redemption={fr},{to}&'
        return self

    def sec_type(self):
        self.__req__ += f'sec_type=stock_corporate_bond,stock_exchange_bond&'
        return self

    def currencyid(self, value='rub'):
        self.__req__ += f'currencyid={value}&'
        return self

    def high_risk(self, value=False):
        if not value:
            self.__req__ += f'high_risk={0}&'
        return self

    def listing(self, listname=[1,2,3]): 
        val = ','.join(map(str, listname))
        self.__req__ += f'listname={val}&'
        return self

    def __str__(self):
        return self.__req__[:-1]
