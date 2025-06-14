from threading import Thread
from time import sleep
from datetime import datetime

class TimeThread(Thread):
    __need_running__ = True
    __accuracy__ = 0.1
    __start__ = datetime.now()
    __now__ = None

    def __init__(self, accuracy=0.1):
        Thread.__init__(self, name="TimeSource")
        self.__accuracy__ = accuracy

    def now(self):
        return self.__now__

    def run(self):
        while self.__need_running__:
            self.__now__ = datetime.now()
            sleep(self.__accuracy__)

    def stop(self):
        self.__need_running__ = False