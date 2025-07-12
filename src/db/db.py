import postgresql
from logger import *

logger = logging.getLogger("SQL")

# from bonds_request import BondsRequest


class Options:
    __name__ = 'options'
    __db__ = None

    def __init__(self, db):
        self.__db__ = db

    def insert(self, name, value):
        res = self.__db__.prepare(f'INSERT INTO {self.__name__} (name, value) SET (\"{name}\", \"{value}\") ON CONFLICT DO UPDATE SET value=\"{value}\";')()
        logger.info(f'Options.insert: {res}')

    def get(self, name):
        res = self.__db__.prepare(f'INSERT INTO {self.__name__} (name, value) SET (\"{name}\", \"{value}\") ON CONFLICT DO UPDATE SET value=\"{value}\";')()

        logger.info(f'Options.get: {res}')
        if len(res) > 0:
            return res[0][1]
        else:
            return None


class Psql:
    __db__ = None
    __options__ = None

    def __init__(self, db_name, user, password, ip='127.0.0.1', port=5432):
        self.__db__ = postgresql.open(f'pq://{user}:{password}@{ip}:{port}/{db_name}')
        self.__options__(self.__db__)

    def save_filters(self, filters: json):
        self.__options__.insert('filters', filters)
