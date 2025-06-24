import sys
import logging

LOG_FORMAT = '%(asctime)s(%(threadName)s) %(levelname)s - %(message)s'

logging.basicConfig(filename='/opt/jbond/jbond.log', level=logging.INFO, format=LOG_FORMAT)
