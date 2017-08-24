import configparser
import  codecs

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

        for i in deps:
            # if i == common.CONFIG:
            #     common.AUTHOR = self.cfg.get(i, common.WHO_S)
            #
            #     print (common.AUTHOR)
            #     continue

            reposLinks = self.cfg.get(i, common.REPOS).split("\n")

            reposList = []

            for j in reposLinks:
                repo = Repo()
                repo.setLink(j)
                reposList.append(repo)

            model.addDep(i, reposList)

        
    def loadCfg(self, fileName, model):
        self.readFile(fileName)

        self.fillModel(model)
