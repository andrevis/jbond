import logging

LOG_FORMAT = '%(asctime)s(%(threadName)s) %(levelname)s - %(message)s'

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
logging.getLogger().addHandler(handler)
