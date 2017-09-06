import configparser

import common_defs
from logger import *
from tag_model import *

__all__ = ['CfgLoader']


class CfgLoader:
    def __init__(self):
        out_log(self.__class__.__name__, "init")
        self.__cfg = configparser.ConfigParser()
        self.__translateFile = common_defs.TRANSLATE_PATH

    def read_file(self, file_name):
        self.__cfg.read(file_name)

    def fill_model(self, model):
        deps = self.__cfg.sections()

        common_defs.OUT_PATH = common_defs.LIN_OUT_P_DEF
        for i in deps:
            prefix = None
            if i == common_defs.CONFIG:
                if self.__cfg.has_option(i, common_defs.OUT_P):
                    common_defs.OUT_PATH = self.__cfg.get(i, common_defs.OUT_P)
                continue

            if self.__cfg.has_option(i, common_defs.PREFIX):
                prefix = self.__cfg.get(i, common_defs.PREFIX)

            repos_links = self.__cfg.get(i, common_defs.REPOS).split("\n")

            repos_list = []

            for j in repos_links:
                repo = Repo()
                repo.name = j
                repo.link = prefix + j
                repos_list.append(repo)

            model.departments[i] = repos_list

        out_log(self.__class__.__name__, "out path: " + common_defs.OUT_PATH)

    def load_mapped_dev_names(self, model):
        f = open(common_defs.TRANSLATE_PATH)

        if f:
            file_text = f.readlines()

            if file_text is not None:
                for line in file_text:
                    name = line.split("=")[:1][-1]
                    tr_name = line.split("=")[1:][-1]
                    model.mappedDevNames[name] = tr_name
        else:
            out_err(self.__class__.__name__, "can't open file with translates: " + common_defs.TRANSLATE_PATH)
        
    def load_config(self, file_name, model):
        self.read_file(file_name)
        self.fill_model(model)

        out_log(self.__class__.__name__, "config was loaded")

        if self.__translateFile:
            self.load_mapped_dev_names(model)
            out_log(self.__class__.__name__, "mapped names was loaded")
