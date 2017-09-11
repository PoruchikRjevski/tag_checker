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
        self.__soft_type = ""

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
        return self.__soft_type

    @prefix.setter
    def prefix(self, prefix):
        self.__soft_type = prefix


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
        self.dev_name = ""
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