import time

from logger import *

__all__ = ['TimeChecker']

class TimeChecker:
    def __init__(self):
        self.__first = 0
        self.__result = 0

    @property
    def start(self):
        self.__first = time.time()
        return None

    @property
    def stop(self):
        self.__result = time.time() - self.__first
        return None

    @property
    def passed_time_str(self):
        return "exec time, s: " + str(round(self.__result, 4))
