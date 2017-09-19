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

        self.__gen_paths()
        self.__set_default_out_path()

    def __gen_paths(self):
        self.__config_def_path = ""

        if g_v.CUR_PLATFORM == c_d.LINUX_P:
            self.__config_def_path = os.path.join(c_d.LIN_CFG_P, c_d.CFG_F_NAME)
        elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
            self.__config_def_path = os.path.join(c_d.WIN_CFG_P, c_d.CFG_F_NAME)

    def __set_default_out_path(self):
        if g_v.CUR_PLATFORM == c_d.LINUX_P:
            g_v.OUT_PATH = c_d.LIN_OUT_P_DEF
        elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
            g_v.OUT_PATH = c_d.WIN_OUT_P_DEF

    def __load_config_block(self, block):
        if self.__cfg.has_option(block, c_d.OUT_P):
            g_v.OUT_PATH = self.__cfg.get(block, c_d.OUT_P)

    def __load_translate_block(self, block, model):
        for name in self.__cfg[block]:
            model.tr_dev_names[name] = self.__cfg.get(block, name)

    def __add_department(self, block, model):
        prefix = ""
        if self.__cfg.has_option(block, c_d.SECT_PREFIX):
            prefix = self.__cfg.get(block, c_d.SECT_PREFIX)

        repos_links = self.__cfg.get(block, c_d.SECT_REPOS).split("\n")

        if repos_links:
            dep = Department(block)

            for repo_name in repos_links:
                repo = Repo()

                pre_link = ""
                splitted = repo_name.split(":")
                if isinstance(splitted, list) and len(splitted) == 2:
                    repo.soft_type = splitted[0]
                    pre_link = splitted[1]
                    if repo.soft_type not in dep.soft_types:
                        dep.soft_types.append(repo.soft_type)
                else:
                    pre_link = repo_name

                repo.link = prefix + pre_link
                repo.name = pre_link
                dep.repos.append(repo)

            model.departments[block] = dep

    def __write_cfg(self):
        with open(self.__config_def_path, 'w') as config_file:
            self.__cfg.write(config_file)

    def open_cfg(self):
        if not os.path.exists(self.__config_def_path):
            out_err(c_d.E_CFNE_STR)
            return c_d.EXIT_CFNE

        self.__cfg = configparser.ConfigParser()
        self.__cfg.read(self.__config_def_path)

        return None


    def load_config(self, model):
        if g_v.DEBUG: out_log("start load config")

        blocks = self.__cfg.sections()

        for block in blocks:
            if block == c_d.BLOCK_CONFIG:
                self.__load_config_block(block)
            elif block == c_d.BLOCK_TRAN:
                self.__load_translate_block(block, model)
            else:
                self.__add_department(block, model)

        if g_v.DEBUG: out_log("config was loaded")

    def show(self, block=""):
        if block:
            if self.__cfg.has_section(block):
                print("Department: {:s}".format(block))

                if block == c_d.BLOCK_TRAN:
                    for name in self.__cfg[block]:
                        print(name, " : ", self.__cfg.get(block, name))
                if block == c_d.BLOCK_CONFIG:
                    pass
                else:
                    if self.__cfg.has_option(block, c_d.SECT_PREFIX):
                        print("Prefix: {:s}".format(self.__cfg.get(block, c_d.SECT_PREFIX)))
                    if self.__cfg.has_option(block, c_d.SECT_REPOS):
                        repos = self.__cfg.get(block, c_d.SECT_REPOS).split("\n")
                        print("Repos:")
                        for repo in repos:
                            print(repo)
        else:
            print("All sections:")
            for sect in self.__cfg.sections():
                print(sect)

    def add_repo(self, block, repos):
        repos_b = ""

        if self.__cfg.has_section(block):
            if self.__cfg.has_option(block, c_d.SECT_REPOS):
                repos_b = self.__cfg[block][c_d.SECT_REPOS] + "\n"
        else:
            self.__cfg[block] = {c_d.SECT_PREFIX : "", c_d.SECT_REPOS : ""}

        if isinstance(repos, list):
            for repo in repos:
                repos_b += "{:s}\n".format(repo)
        else:
            repos_b += "{:s}\n".format(repos)

        self.__cfg[block][c_d.SECT_REPOS] = repos_b

        self.__write_cfg()

    def rem_repo(self, block, repos):
        repos_b = ""

        if self.__cfg.has_section(block):
            if self.__cfg.has_option(block, c_d.SECT_REPOS):
                repos_b = self.__cfg[block][c_d.SECT_REPOS]

                if isinstance(repos, list):
                    for repo in repos:
                        repos_b = repos_b.replace(repo, "").rstrip().lstrip()
                else:
                    repos_b = repos_b.replace(repos, "").rstrip().lstrip()

                self.__cfg[block][c_d.SECT_REPOS] = repos_b

                self.__write_cfg()

    def add_translate(self, name, tr_name):
        if not self.__cfg.has_section(c_d.BLOCK_TRAN):
            self.__cfg[c_d.BLOCK_TRAN] = {}

        pairs = ""
        if self.__cfg.has_option(c_d.BLOCK_TRAN, c_d.SECT_PAIRS):
            pairs = self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS]

        if name not in pairs:
            self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS] = pairs + "{:s}:{:s}|".format(name, tr_name)
        else:
            tr_dict = dict(item.split(":") for item in pairs.split("|") if item)

            tr_dict[name] = tr_name

            pairs = "|".join("{:s}:{:s}".format(key, value) for key, value in tr_dict.items())

            self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS] = pairs

        self.__write_cfg()

    def rem_translate(self, translates):
        if self.__cfg.has_section(c_d.BLOCK_TRAN):
            if self.__cfg.has_option(c_d.BLOCK_TRAN, c_d.SECT_PAIRS):
                pairs = self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS]
                tr_dict = dict(item.split(":") for item in pairs.split("|") if item)

                if isinstance(translates, list):
                    for tr in translates:
                        if tr in tr_dict.keys():
                            del tr_dict[tr]
                else:
                    del tr_dict[translates]

                if not tr_dict:
                    del self.__cfg[c_d.BLOCK_TRAN]

                pairs = "|".join("{:s}:{:s}".format(key, value) for key, value in tr_dict.items())

                self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS] = pairs

                self.__write_cfg()

    def add_department(self, departments):
        if isinstance(departments, list):
            for dep in departments:
                if not self.__cfg.has_section(dep):
                    self.__cfg[dep] = {}
        else:
            self.__cfg[departments] = {}

        self.__write_cfg()

    def rem_department(self, departments):
        if isinstance(departments, list):
            for dep in departments:
                if self.__cfg.has_section(dep):
                    del self.__cfg[dep]
        else:
            del self.__cfg[departments]

        self.__write_cfg()

    def change_prefix(self, department, prefix):
        if self.__cfg.has_section(department):
            self.__cfg[department][c_d.SECT_PREFIX] = prefix

            self.__write_cfg()