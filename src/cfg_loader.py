import os
import configparser

import common_defs as c_d
import global_vars as g_v
from logger import *
from tag_model import *

__all__ = ['CfgLoader']


class CfgLoader:
    def __init__(self):
        if g_v.DEBUG: out_log("init")
        self.__cfg = configparser.ConfigParser()
        self.__trFilePathDef = ""
        self.__cfgFilePathDef = ""

        self.__gen_paths()
        self.__set_default_out_path()

    def is_conf_file_exist(file_name):
        return os.path.exists(file_name)

    def __gen_paths(self):
        if g_v.CUR_PLATFORM == c_d.LINUX_P:
            self.__cfgFilePathDef = os.path.join(c_d.LIN_CFG_P, c_d.CFG_F_NAME)
            self.__trFilePathDef = os.path.join(c_d.LIN_CFG_P, c_d.TR_F_NAME)
        elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
            self.__cfgFilePathDef = os.path.join(c_d.WIN_CFG_P, c_d.CFG_F_NAME)
            self.__trFilePathDef = os.path.join(c_d.WIN_CFG_P, c_d.TR_F_NAME)

    def __read_file(self, file_name):
        name = file_name

        if name is "":
            name = self.__cfgFilePathDef

        if not os.path.exists(name):
            out_err(c_d.E_CFNE_STR)
            return c_d.EXIT_CFNE

        self.__cfg.read(name)

        return None


    def __set_default_out_path(self):
        if g_v.CUR_PLATFORM == c_d.LINUX_P:
            g_v.OUT_PATH = c_d.LIN_OUT_P_DEF
        elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
            g_v.OUT_PATH = c_d.WIN_OUT_P_DEF

    def __fill_model_ex(self, model):
        deps = self.__cfg.sections()

        for i in deps:
            prefix = None
            if i == c_d.CONFIG:
                if self.__cfg.has_option(i, c_d.OUT_P):
                    g_v.OUT_PATH = self.__cfg.get(i, c_d.OUT_P)
                continue

            if self.__cfg.has_option(i, c_d.PREFIX):
                prefix = self.__cfg.get(i, c_d.PREFIX)

            repos_links = self.__cfg.get(i, c_d.REPOS).split("\n")

            repos_list = []

            for j in repos_links:
                repo = Repo_ex()
                repo.name = j
                repo.link = prefix + j
                repos_list.append(repo)

            model.departments[i] = repos_list

        if g_v.DEBUG: out_log("out path: " + g_v.OUT_PATH)

    def __fill_model(self, model):
        blocks = self.__cfg.sections()

        for blk in blocks:
            if blk == c_d.CONFIG:
                if self.__cfg.has_option(blk, c_d.OUT_P):
                    g_v.OUT_PATH = self.__cfg.get(blk, c_d.OUT_P)
                continue

            prefix = ""
            if self.__cfg.has_option(blk, c_d.PREFIX):
                prefix = self.__cfg.get(blk, c_d.PREFIX)

            repos_links = self.__cfg.get(blk, c_d.REPOS).split("\n")

            if repos_links:
                dep = Department(blk)

                for repo_name in repos_links:
                    repo = Repo(repo_name)

                    pre_link = ""
                    splitted = repo_name.split(":")
                    if isinstance(splitted, list) and len(splitted) == 2:
                        repo.prefix = splitted[0]
                        pre_link = splitted[1]

                        dep.soft_types[splitted[0]] = []
                    else:
                        pre_link = repo_name

                    repo.link = prefix + pre_link
                    dep.repos.append(repo)

                model.departments[blk] = dep

        if g_v.DEBUG: out_log("out path: " + g_v.OUT_PATH)


    def __load_tr_dev_names(self, model):
        tr_f = open(self.__trFilePathDef)

        if tr_f:
            file_text = tr_f.readlines()

            if file_text is not None:
                for line in file_text:
                    name = line.split("=")[:1][-1]
                    tr_name = line.split("=")[1:][-1]
                    model.tr_dev_names[name] = tr_name
        else:
            out_err("can't open file with translates: " + self.__trFilePathDef)
        
    def load_config(self, file_name, model):
        res = self.__read_file(file_name)
        if res is not None:
            return res

        if g_v.DEBUG: out_log("start load config")

        self.__fill_model(model)

        if g_v.DEBUG: out_log("config was loaded")

        if self.__trFilePathDef:
            self.__load_tr_dev_names(model)

            if g_v.DEBUG: out_log("mapped names was loaded")
