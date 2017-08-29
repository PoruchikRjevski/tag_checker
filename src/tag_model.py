import collections

import common
from logger import out_log, out_err


# deps it is dict of (department, list of repos)
class TagModel:
    def __init__(self):
        out_log(self.__class__.__name__, "init")
        self.deps = collections.OrderedDict()

        self.mappedDevNames = {}

    def add_mapped_device_names(self, key, val):
        self.mappedDevNames[key] = val

    def get_mapped_device_name(self, name):
        if name in self.mappedDevNames:
            return self.mappedDevNames[name]
        return name

    def add_department(self, key, val):
        self.deps[key] = val

    def get_departments(self):
        return self.deps


class Repo:
    def __init__(self):
        self.devices = collections.OrderedDict()
        self.link = " "

    def add_to_device(self, name, note):
        self.devices[name].add_to_history(note)

    def add_device_by_name(self, name, dev):
        self.devices[name] = dev

    def get_devices(self):
        return self.devices

    def set_link(self, link):
        self.link = link

    def get_link(self):
        return self.link


class Device:
    def __init__(self):
        self.history = []       # list if Notes
        self.last = []          # list if Notes
        self.items = []         # list of Notes by items
        self.name = ""          # name from repo
        self.trName = ""        # translated name

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_mapped_name(self, trName):
        self.trName = trName

    def get_mapped_name(self):
        return self.trName

    def add_to_history(self, note):
        self.history.append(note)

    def get_history(self):
        return self.history

    def sort_history(self):
        self.history = sorted(self.history, key=lambda note: note.date, reverse=True)

    def fill_last(self):
        for type in common.TYPES_L:
            first = True
            lastDate = 0
            for note in self.history:
                if note.type == type:
                    if first:
                        first = False
                        lastDate = note.date
                    if note.date == lastDate:
                        self.add_to_last(note)

    def add_to_last(self, note):
        self.last.append(note)

    def get_last(self):
        return self.last

    def get_last_num_by_type(self, type):
        res = 0
        for note in self.last:
            if type == note.type:
                res += 1
        return res


class Note:
    def __init__(self):
        self.type = common.TYPE_ALL
        self.tag = ""
        self.name = ""
        self.num = -1
        self.date = -1
        self.sHash = -1
        self.commDate = -1
        self.author = ""
        self.valid = False