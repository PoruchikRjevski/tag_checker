import time

__all__ = ['TimeChecker']


MIN_ID = 0
MAX_ID = 250
last_id = 0

t_id_list = {}

#
# def gen_id():
#     if last_id == MAX_ID:
#         last_id = MIN_ID
#     else:
#         while last_id not in t_id_list.keys():
#             last_id += 1


def get_token():
    pass
    # generate id with respective to t_id_list including
    # write to t_id_list 0 by id key


def start(id):
    pass
    # write to t_id_list start time by id key


def stop(id):
    pass
    # write to t_id_list diff betw stop and start time by id key


def get_passed_time_str():
    pass

def start():
    pass
    # gen id with respective to t_id_list including
    # add item to t_id_list with start value




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
        return "{:s}(sec)".format(str(round(self.__result, 4)))
