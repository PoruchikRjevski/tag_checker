from collections import OrderedDict
from queue import Queue

import common_defs as c_d
import global_vars as g_v

__all__ = ['TagModel', 'Department', 'Repo', 'Device', 'Item', 'CommitInfo', 'UPDATE_FLAG', 'REPO_OBJECT']


UPDATE_FLAG = 'update_flag'
REPO_OBJECT = 'repo_object'


class TagModel:
    """
    __departments               is ordered {dep_name, Department object}
    __tr_dev_names              is {orig_name, tr_name}
    """
    def __init__(self):
        self.__departments = OrderedDict()
        self.__tr_dev_names = {}

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
    __repos                     is [{repo: flag_updated}...]
    __commits                   is [CommitInfo object]
    __items                     is [Item...]
    __devices                   is {dev: flag_updated}
    __soft_types                is [type...]
    """
    def __init__(self, name=""):
        self.__name = name
        self.__repos = []
        self.__commits = []
        self.__items = []
        self.__devices = {}
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
    __sw_archive_module_id      software archive module identifier
    """
    def __init__(self):
        self.__name = ""
        self.__link = ""
        self.__soft_type = ""
        self.__sw_archive_module_id = ""
        self.__sw_archive_module_group_id = ""

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

    @property
    def sw_archive_module_id(self):
        return self.__sw_archive_module_id

    @sw_archive_module_id.setter
    def sw_archive_module_id(self, sw_archive_module_id):
        self.__sw_archive_module_id = sw_archive_module_id

    @property
    def sw_archive_module_group_id(self):
        return self.__sw_archive_module_group_id

    @sw_archive_module_group_id.setter
    def sw_archive_module_group_id(self, sw_archive_module_group_id):
        self.__sw_archive_module_group_id = sw_archive_module_group_id


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
        self.tag_class = c_d.TAG_CLASS_PROD
        self.device_class = ""
        self.device_selector_id = -1
        self.device_selector_type = c_d.TAG_DEVICE_SELECTOR_TYPE_ALL
        self.tag = ""
        self.tag_date = ""
        self.tag_date_obj = None
        self.tag_date_ord = 0
        self.commit_hash_short = ""
        self.commit_hash_full = None
        self.solution_domain = "/"
        self.valid = False
        self.repo_index = -1
        self.commit_index = -1
        self.metric = MetricsInfo()

    def is_base(self):
        return self.device_selector_type == c_d.TAG_DEVICE_SELECTOR_TYPE_ALL

    def is_prod(self):
        return self.device_class == c_d.TAG_CLASS_PROD

    def is_test(self):
        return self.device_class == c_d.TAG_CLASS_TEST

    def is_base_prod(self):
        return self.is_base() and self.is_prod()

    def is_base_test(self):
        return self.is_base() and self.is_test()

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
        self.repo_index = -1


class MetricsInfo:
    def __init__(self):
        """
        forced                  if tag not in develop
        last                    if it is the last version of soft
        jumps                   number of commits between this and last if this is not last
        """
        self.forced = False # if tag not in develop
        self.last = False # if it is the last version of soft
        self.exp = False # if item or order version newer than base version(if it exist)
        self.old = False
        self.jumps = 0 # number of commits between this and last if this is not last
        self.color_intensity = 1 # multiplier for red color step+ for shows metric
        self.diff_d = None # number of days between this and last if this is not last
