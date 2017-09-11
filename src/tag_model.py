from collections import OrderedDict
from queue import Queue

import common_defs as c_d
import global_vars as g_v
from logger import *

__all__ = ['TagModel', 'Department', 'Repo', 'Device', 'Item']


class TagModel:
    """
    __departments           is ordered {dep_name, Department object}
    __tr_dev_names          is {orig_name, tr_name}
    """
    def __init__(self):
        self.__departments = OrderedDict()
        self.__tr_dev_names = {}

        if g_v.DEBUG: out_log("inited")

    def get_tr_dev_name(self, key=None):
        if key:
            if key in self.__tr_dev_names:
                return self.__tr_dev_names[key]
            else:
                return key
        return self.__tr_dev_names

    @property
    def tr_dev_names(self):
        return self.get_tr_dev_name()

    @property
    def departments(self):
        return self.__departments


class Department:
    """
    __name                  is name of department from config
    __repos                 is [Repo...]
    __domains               is {domain, [dev_indexes]}
    __soft_types            is {soft_type, [dev_indexes]}
    """
    def __init__(self, name=""):
        self.__name = name
        self.__repos = []
        self.__devices = []
        self.__domains = {}
        self.__soft_types = {}

    @property
    def repos(self):
        return self.__repos

    @property
    def devices(self):
        return self.__devices

    @property
    def domains(self):
        return self.__domains

    @property
    def soft_types(self):
        return self.__soft_types

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


class Repo:
    """
    __name                  is repo name
    __link                  is link to location
    __prefix                is belong to type of soft
    """
    def __init__(self, name=""):
        self.__name = name
        self.__link = ""
        self.__prefix = ""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
        if c_d.REPO_SUFFIX not in name:
            self.__name += c_d.REPO_SUFFIX

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, link):
        self.__link = link

    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, prefix):
        self.__prefix = prefix


class Device:
    """
    __name                      is device name
    __items                     is [Items objects]
    """
    def __init__(self):
        self.__name = ""
        self.__items = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def items(self):
        return self.__items


class Item:
    """
    describes one item
    """
    def __init__(self):
        self.item_num = -1
        self.item_type = c_d.TYPE_ALL
        self.tag = ""
        self.tag_date = ""
        self.cm_hash = ""
        self.cm_date = ""
        self.cm_msg = ""
        self.cm_auth = ""
        self.p_hash = ""
        self.platform = c_d.D_LINUX
        self.validity = False
        self.repo_i = -1


class Repo_ex:
    def __init__(self):
        self.__devices = OrderedDict()
        self.__link = ""
        self.__name = ""

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name
        if c_d.REPO_SUFFIX not in name:
            self.__name += c_d.REPO_SUFFIX

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


class Device_ex:
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
            self.orders[key].sort(key=lambda note: note.date, reverse=True)

    def fill_last(self):
        for m_type in c_d.TYPES_L:
            to_sort = []
            for num, notes in self.orders.items():
                if notes[0].type == m_type:
                    to_sort.append(notes[0])
            to_sort.sort(key=lambda note: note.num, reverse=False)
            self.lastOrders = to_sort

# struct with info for one tag
class Note:
    def __init__(self):
        self.type = c_d.TYPE_ALL
        self.tag = None
        self.name = None
        self.num = -1
        self.date = ""
        self.sHash = -1
        self.pHash = -1
        self.commDate = -1
        self.commMsg = None
        self.author = None
        self.valid = False
        self.platform = ""


