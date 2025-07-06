import requests
import pandas
import io
from logger import *

logger = logging.getLogger("Defaults")

class DefaultsGetter:

    @staticmethod
    def get(isin):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'close',
            'DNT': '1',
            'Host': 'web.moex.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        }

        url = "https://web.moex.com/moex-web-icdb-api/api/v1/export/site-defaults/xlsx"
        response = requests.get(url, timeout=5, headers=headers)
        if response.status_code != 200:
            logger.error(f'Cannot get MOEX defaults (code={response.status_code}): {response.reason}')
            return None

        excel_data = pandas.read_excel(io.BytesIO(response.content), usecols=['ISIN', 'Состояние', 'Плановая дата'])

        records = excel_data.to_dict(orient='records')
        records = list(filter(lambda record : record['ISIN'] == isin, records))
        records = list(map(lambda record : record['Плановая дата'], records))
        return records
