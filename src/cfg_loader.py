import configparser

from tag_model import TagModel
from tag_model import Tag
from tag_model import Repo

REPOS = "repos"

class CfgLoader:
    def __init__(self):
        self.cfg = configparser.ConfigParser()

    def readFile(self, fileName):
        self.cfg.read(fileName)

    def fillModel(self, model):
        deps = self.cfg.sections()

        depDict = {}

        for i in deps:
            repos = self.cfg.get(i, REPOS).split("\n")

            depDict[i] = []

            for j in repos:

                repo = Repo()
                repo.setLink(j)
                depDict[i].append(repo)

        model.addDeps(depDict)
        
    def loadCfg(self, fileName, model):
        self.readFile(fileName)

        self.fillModel(model)
