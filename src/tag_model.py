from collections import OrderedDict
from queue import Queue

import common_defs as c_d
import global_vars as g_v
from logger import *

__all__ = ['TagModel', 'Department', 'Repo', 'Device', 'Item', 'CommitInfo']


class TagModel:
    """
    __departments               is ordered {dep_name, Department object}
    __tr_dev_names              is {orig_name, tr_name}
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

    def get_tr_dev(self, dev_name):
        if dev_name in self.__tr_dev_names:
            return self.__tr_dev_names[dev_name]
        else:
            return dev_name

    @property
    def departments(self):
        return self.__departments


class Department:
    """
    __name                      is name of department from config
    __repos                     is [Repo...]
    __commits                   is [CommitInfo object]
    __items                     is [Item...]
    __devices                   is [dev_1...dev_n]
    __soft_types                is [type...]
    """
    def __init__(self, name=""):
        self.__name = name
        self.__repos = []
        self.__commits = []
        self.__items = []
        self.__devices = []
        self.__soft_types = [""]

    @property
    def repos(self):
        return self.__repos

    @property
    def commits(self):
        return self.__commits

    @property
    def items(self):
        return self.__items

    @property
    def devices(self):
        return self.__devices

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
    __name                      is repo name
    __link                      is link to location
    __soft_type                 is belong to type of soft
    """
    def __init__(self):
        self.__name = ""
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
    def soft_type(self):
        return self.__soft_type

    @soft_type.setter
    def soft_type(self, soft_type):
        self.__soft_type = soft_type


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
        self.tag_date_obj = None
        self.tag_date_ord = 0
        self.cm_hash = ""
        self.platform = c_d.D_LINUX
        self.valid = False
        self.repo_i = -1
        self.cm_i = -1
        self.metric = MetricsInfo()


class CommitInfo:
    """
    describes info about commit
    """
    def __init__(self):
        self.hash = ""
        self.p_hash = ""
        self.date = ""
        self.date_full = ""
        self.date_obj = None
        self.msg = ""
        self.auth = ""
        self.valid = False
        self.repo_i = -1


class MetricsInfo:
    def __init__(self):
        """
        forced                  if tag not in develop
        last                    if it is the last version of soft
        jumps                   number of commits between this and last if this is not last
        """
        self.forced = False # if tag not in develop
        self.last = False # if it is the last version of soft
        self.jumps = 0 # number of commits between this and last if this is not last
        self.diff_d = None # number of days between this and last if this is not last
