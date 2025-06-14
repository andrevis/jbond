import sys
import logging

LOG_FORMAT = '%(asctime)s(%(threadName)s) %(levelname)s - %(message)s'

logging.basicConfig(filename='/opt/jbond/jbond.log', level=logging.INFO)

# logger = logging.getLogger(__name__)

# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
# logging.getLogger().addHandler(handler)
