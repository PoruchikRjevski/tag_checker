import configparser

import common

from tag_model import TagModel
from tag_model import Repo

class CfgLoader:
    def __init__(self):
        self.cfg = configparser.ConfigParser()

    def readFile(self, fileName):
        self.cfg.read(fileName)

    def fillModel(self, model):
        deps = self.cfg.sections()

        depDict = {}
        sortedList = []

        for i in deps:
            sortedList.append(i)
            repos = self.cfg.get(i, common.REPOS).split("\n")

            depDict[i] = []

            for j in repos:
                repo = Repo()
                repo.setLink(j)
                depDict[i].append(repo)

        model.addDeps(depDict)
        model.setSortedList(sortedList)
        
    def loadCfg(self, fileName, model):
        self.readFile(fileName)

        self.fillModel(model)
