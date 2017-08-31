import configparser

import common
from logger import out_log, out_err
from tag_model import TagModel, Repo


class CfgLoader:
    def __init__(self):
        out_log(self.__class__.__name__, "init")
        self.cfg = configparser.ConfigParser()
        self.translateFile = common.TRANSLATE_PATH

    def read_file(self, fileName):
        self.cfg.read(fileName)

    def fill_model(self, model):
        deps = self.cfg.sections()

        common.OUT_PATH = common.OUT_PATH_DEF
        for i in deps:
            prefix = ""
            if i == common.CONFIG:
                if self.cfg.has_option(i, common.OUT_P):
                    common.OUT_PATH = self.cfg.get(i, common.OUT_P)

                continue

            if self.cfg.has_option(i, common.PREFIX):
                prefix = self.cfg.get(i, common.PREFIX)

            reposLinks = self.cfg.get(i, common.REPOS).split("\n")

            reposList = []

            for j in reposLinks:
                repo = Repo()
                repo.name = j
                # repo.set_name(j)
                repo.link = prefix + j
                # repo.set_link(prefix + j)
                reposList.append(repo)

            model.departments[i] = reposList
            # model.add_department(i, reposList)

        out_log(self.__class__.__name__, "out path: " + common.OUT_PATH)

    def load_mapped_dev_names(self, model):
        f = open(common.TRANSLATE_PATH)

        if f:
            fileText = f.readlines()

            if fileText:
                for line in fileText:
                    name = line.split("=")[:1][-1]
                    trName = line.split("=")[1:][-1]
                    model.mappedDevNames[name] = trName
                    # model.add_mapped_device_names(line.split("=")[:1][-1], line.split("=")[1:][-1])
        else:
            out_err(self.__class__.__name__, "can't open file with translates: " + common.TRANSLATE_PATH)
        
    def load_config(self, fileName, model):
        self.read_file(fileName)
        self.fill_model(model)

        out_log(self.__class__.__name__, "config was loaded")

        if self.translateFile:
            self.load_mapped_dev_names(model)
            out_log(self.__class__.__name__, "mapped names was loaded")
