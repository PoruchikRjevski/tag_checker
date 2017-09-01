from collections import OrderedDict

import common
from logger import *

__all__ = ['TagModel', 'Repo', 'Device', 'Note']

# __departments contain [repos] by name of department
class TagModel:
    def __init__(self):
        out_log(self.__class__.__name__, "init")
        self.__departments = OrderedDict()

        self.__mappedDevNames = {}

    def get_mappedDevName(self, key=None):
        if key:
            if key in self.__mappedDevNames:
                return self.__mappedDevNames[key]
            else:
                return key
        return self.__mappedDevNames

    @property
    def mappedDevNames(self):
        return self.get_mappedDevName()

    @property
    def departments(self):
        return self.__departments


class Repo:
    def __init__(self):
        self.__devices = OrderedDict()
        self.__link = None
        self.__name = None

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name
        if common.REPO_SUFFIX not in name:
            self.__name += common.REPO_SUFFIX

    @property
    def link(self):
        return self.__link
    @link.setter
    def link(self, link):
        self.__link = link

    @property
    def devices(self):
        return self.__devices

    def add_device(self, name, dev):
        self.devices[name] = dev

    def add_to_device(self, name, note):
        self.devices[name].add_order(note)


class Device:
    def __init__(self):
        self.__lastOrders = []                      # list if Notes
        self.__orders = OrderedDict()               # list of Notes by items
        self.__name = ""                            # name from repo
        self.__trName = ""                          # translated name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def trName(self):
        return self.__trName

    @trName.setter
    def trName(self, tr_name):
        self.__trName = tr_name

    @property
    def orders(self):
        return self.__orders

    def add_order(self, note):
        if note.num in self.orders:
            self.orders[note.num].append(note)
        else:
            self.orders[note.num] = [note]

    @property
    def lastOrders(self):
        return self.__lastOrders

    @lastOrders.setter
    def lastOrders(self, adding):
        self.__lastOrders += adding

    def get_cnt_by_num(self, number):
        return len(self.orders[number])

    def sort_orders(self):
        for key, val in self.orders.items():
            self.orders[key] = sorted(val, key=lambda note: note.date, reverse=True)

    def fill_last(self):
        for m_type in common.TYPES_L:
            to_sort = []
            for num, notes in self.orders.items():
                if notes[0].type == m_type:
                    to_sort.append(notes[0])
            to_sort = sorted(to_sort, key=lambda note: note.num, reverse=False)
            self.lastOrders = to_sort

# struct with info for one tag
class Note:
    def __init__(self):
        self.type = common.TYPE_ALL
        self.tag = None
        self.name = None
        self.num = -1
        self.date = -1
        self.sHash = -1
        self.pHash = -1
        self.commDate = -1
        self.commMsg = None
        self.author = None
        self.valid = False
