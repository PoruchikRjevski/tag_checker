import collections

import common

# deps it is dict of (department, list of repos)
class TagModel:
    def __init__(self):
        self.deps = collections.OrderedDict()

        self.mappedDevNames = {}

    def addMappedDevNames(self, key, val):
        self.mappedDevNames[key] = val

    def getMappedDevName(self, name):
        if name in self.mappedDevNames:
            return self.mappedDevNames[name]
        return name

    def addDep(self, key, val):
        self.deps[key] = val

    def getDeps(self):
        return self.deps

class Repo:
    def __init__(self):
        self.devices = collections.OrderedDict()
        self.link = " "

    def addToDevice(self, name, note):
        self.devices[name].addToHistory(note)

    def addDeviceByName(self, name, dev):
        self.devices[name] = dev

    def getDevices(self):
        return self.devices

    def setLink(self, link):
        self.link = link

    def getLink(self):
        return self.link

class Device:
    def __init__(self):
        self.history = [] # list if Notes
        self.last = [] # list if Notes
        self.items = [] # list of Notes by items
        self.name = "" # name from repo
        self.trName = "" # translated name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setTrName(self, trName):
        self.trName = trName

    def getTrName(self):
        return self.trName

    def addToHistory(self, note):
        self.history.append(note)

    def getHistory(self):
        return self.history

    def sortHistory(self):
        self.history = sorted(self.history, key=lambda note: note.date, reverse=True)

    def fillLast(self):
        for type in common.TYPES_L:
            first = True
            lastDate = 0
            for note in self.history:
                if note.type == type:
                    if first:
                        first = False
                        lastDate = note.date
                    if note.date == lastDate:
                        self.addToLast(note)

    def addToLast(self, note):
        self.last.append(note)

    def getLast(self):
        return self.last

    def getLastNumByType(self, type):
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