import configparser
import os
import  codecs

import common

from tag_model import TagModel
from tag_model import Repo

class CfgLoader:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.translateFile = ""

    def readFile(self, fileName):
        self.cfg.read(fileName)

    def fillModel(self, model):
        deps = self.cfg.sections()

        for i in deps:
            if i == common.CONFIG:
                if self.cfg.has_option(i, common.OUT_P):
                    common.OUT_PATH = self.cfg.get(i, common.OUT_P)
                    #if not os.path.isabs(common.OUT_PATH):
                    #    common.OUT_PATH = os.path.abspath(common.OUT_PATH)
                if self.cfg.has_option(i, common.TRANSLATE_PATH):
                    self.translateFile = self.cfg.get(i, common.TRANSLATE_PATH)

                continue

            reposLinks = self.cfg.get(i, common.REPOS).split("\n")

            reposList = []

            for j in reposLinks:
                repo = Repo()
                repo.setLink(j)
                reposList.append(repo)

            model.addDep(i, reposList)

    def loadMapped(self, model):
        f = open(self.translateFile)

        if f:
            fileText = f.readlines()

            if fileText:
                for line in fileText:
                    model.addMappedDevNames(line.split("=")[:1][-1], line.split("=")[1:][-1])
        
    def loadCfg(self, fileName, model):
        self.readFile(fileName)

        self.fillModel(model)

        if self.translateFile:
            self.loadMapped(model)
