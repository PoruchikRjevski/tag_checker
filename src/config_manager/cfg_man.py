import os
import configparser

import common_defs as c_d
import global_vars as g_v
from logger import *
from tag_model import *
from cmd_executor.cmd_executor import *

__all__ = ['CfgLoader']


# TODO: maybe json will be simpler?

class CfgLoader:

    def __init__(self):
        if g_v.DEBUG: out_log("init")  # TODO: used logger?

        self.__cfg = None
        self.__gen_paths()
        CfgLoader.__set_default_out_path()

    def __gen_paths(self):
        self.__config_def_path = ""

        if g_v.CUR_PLATFORM == c_d.LINUX_P:
            self.__config_def_path = os.path.join(c_d.LIN_CFG_P, c_d.CFG_F_NAME)
        elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
            self.__config_def_path = os.path.join(c_d.WIN_CFG_P, c_d.CFG_F_NAME)

    @staticmethod
    def __set_default_out_path():
        if g_v.CUR_PLATFORM == c_d.LINUX_P:
            g_v.OUT_PATH = c_d.LIN_OUT_P_DEF
        elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
            g_v.OUT_PATH = c_d.WIN_OUT_P_DEF

    def __try_load(self, block, item, default_value):
        if self.__cfg.has_option(block, item):
            return self.__cfg.get(block, item)
        else:
            return default_value

    def __load_config_block(self, block):
        g_v.OUT_PATH = self.__try_load(block, c_d.OUT_P, g_v.OUT_PATH)
        g_v.DIST_LINK_PREFIX = self.__try_load(block, c_d.SECT_DIST_LINK_PREFIX, g_v.DIST_LINK_PREFIX)
        g_v.DIST_LINK_PATTERN = self.__try_load(block, c_d.SECT_DIST_LINK_PATTERN, g_v.DIST_LINK_PATTERN)

    def __load_translate_block(self, block, model):
        if self.__cfg.has_option(block, c_d.SECT_PAIRS):
            pairs = self.__cfg.get(block, c_d.SECT_PAIRS)
            tr_dict = dict(item.split(":") for item in pairs.split("|") if item)

            model.tr_dev_names.update(tr_dict)
        # for name in self.__cfg[block]:
        #     model.tr_dev_names[name] = self.__cfg.get(block, name)

    @staticmethod
    def get_sw_module_uid_from_repo_full_link(repo_full_link):

        id = repo_full_link

        std_prefix = "/home/git/repositories/"
        std_suffix = ".git"

        if id.startswith(std_prefix):
            id = id[len(std_prefix):]

        if id.endswith(std_suffix):
            id = id[:-len(std_suffix)]

        return id

    @staticmethod
    def get_sw_module_id_from_repo_full_link(repo_full_link):
        id = CfgLoader.get_sw_module_uid_from_repo_full_link(repo_full_link)
        return os.path.basename(id)

    @staticmethod
    def get_sw_module_group_id_from_repo_full_link(repo_full_link):
        id = CfgLoader.get_sw_module_uid_from_repo_full_link(repo_full_link)
        id = os.path.split(id)
        if len(id) > 1:
            return id[0]
        else:
            return ""

    def __get_dep_prefix(self, dep):
        if self.__cfg.has_option(dep, c_d.OPTION_PREFIX):
            return self.__cfg.get(dep, c_d.OPTION_PREFIX)

        return ""

    def __add_department(self, block, model):
        prefix = ""
        prefix = self.__get_dep_prefix(block)

        repos_links = self.__cfg.get(block, c_d.OPTION_REPOS).split("\n")

        if repos_links:
            dep = Department(block)

            for repo_name in repos_links:
                repo = Repo()

                split = repo_name.split(":")
                item_count = len(split)
                sw_archive_module_id = ""
                sw_archive_module_group_id = ""
                if isinstance(split, list) and item_count > 1:
                    repo.soft_type = split[0]

                    if repo.soft_type not in dep.soft_types:
                        dep.soft_types.append(repo.soft_type)
                    pre_link = split[1]
                    if item_count > 2:
                        sw_archive_module_group_id = split[2]
                    if item_count > 3:
                        sw_archive_module_id = split[3]
                else:
                    pre_link = repo_name

                repo.link = prefix + pre_link
                repo.name = pre_link
                
                if not sw_archive_module_id:
                    repo.sw_archive_module_id = CfgLoader.get_sw_module_id_from_repo_full_link(repo.link)
                else:
                    repo.sw_archive_module_id = sw_archive_module_id

                if not sw_archive_module_group_id:
                    sw_archive_module_group_id = CfgLoader.get_sw_module_group_id_from_repo_full_link(repo.link)

                if len(sw_archive_module_group_id) > 0:
                    sw_archive_module_group_id = sw_archive_module_group_id + "/"
                
                repo.sw_archive_module_group_id = sw_archive_module_group_id
                dep.repos.append(repo)

            model.departments[block] = dep

    def __write_cfg(self):
        with open(self.__config_def_path, 'w') as config_file:
            self.__cfg.write(config_file)

    @staticmethod
    def __separate_repo_and_soft_type(repo):
        splitted = repo.split(":")

        soft_type = ""
        repo_name = ""

        if isinstance(splitted, list) and len(splitted) > 1:
            soft_type = splitted[0]
            repo_name = splitted[1]
        else:
            repo_name = repo

        return soft_type, repo_name

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
                elif block == c_d.BLOCK_CONFIG:
                    pass
                else:
                    if self.__cfg.has_option(block, c_d.OPTION_PREFIX):
                        print("Prefix: {:s}".format(self.__cfg.get(block, c_d.OPTION_PREFIX)))
                    if self.__cfg.has_option(block, c_d.OPTION_REPOS):
                        repos = self.__cfg.get(block, c_d.OPTION_REPOS).split("\n")
                        print("Repos:")
                        for repo in repos:
                            print(repo)
        else:
            print("All sections:")
            for sect in self.__cfg.sections():
                print(sect)

    def __get_repo_path(self, dep, repo):
        path = ""

        if self.__cfg.has_section(dep):
            path = self.__get_dep_prefix(dep)

        return os.path.join(path, repo)

    def add_git_hooks(self, dep, repo):
        _, repo = self.__separate_repo_and_soft_type(repo)

        hooks_path = os.path.join(c_d.GIT_HOOKS_PATH, c_d.POST_RX_HOOK_NAME)

        repo_path = self.__get_repo_path(dep, repo)
        repo_hooks_dir_path = os.path.join(repo_path, c_d.HOOKS_PATH)

        run_cmd("yes | cp -rf {:s} {:s}".format(hooks_path, repo_hooks_dir_path))

    def rem_git_hooks(self, dep, repo):
        _, repo = self.__separate_repo_and_soft_type(repo)

        repo_path = self.__get_repo_path(dep, repo)
        hook_path = os.path.join(repo_path, c_d.HOOKS_PATH, c_d.POST_RX_HOOK_NAME)

        run_cmd("rm -f {:s}".format(hook_path))

    def add_repo(self, block, repos):
        if not block or not repos:
            return

        repos_b = ""

        if self.__cfg.has_section(block):
            if self.__cfg.has_option(block, c_d.OPTION_REPOS):
                repos_b = self.__cfg[block][c_d.OPTION_REPOS] + "\n"
        else:
            self.__cfg[block] = {c_d.OPTION_PREFIX : "", c_d.OPTION_REPOS : ""}

        if isinstance(repos, list):
            for repo in repos:
                repos_b += "{:s}\n".format(repo)

                self.add_git_hooks(block, repo)
        else:
            repos_b += "{:s}\n".format(repos)
            self.add_git_hooks(block, repos)

        self.__cfg[block][c_d.OPTION_REPOS] = repos_b

        self.__write_cfg()

    def rem_repo(self, block, repos):
        if not block or not repos:
            return

        repos_b = ""

        if self.__cfg.has_section(block):
            if self.__cfg.has_option(block, c_d.OPTION_REPOS):
                repos_b = self.__cfg[block][c_d.OPTION_REPOS]

                if isinstance(repos, list):
                    for repo in repos:
                        repos_b = repos_b.replace(repo, "").rstrip().lstrip()
                        self.rem_git_hooks(block, repo)
                else:
                    repos_b = repos_b.replace(repos, "").rstrip().lstrip()
                    self.rem_git_hooks(block, repos)

                self.__cfg[block][c_d.OPTION_REPOS] = repos_b

                self.__write_cfg()

    def add_translate(self, name, tr_name):
        if not self.__cfg.has_section(c_d.BLOCK_TRAN):
            self.__cfg[c_d.BLOCK_TRAN] = {}

        pairs = ""
        if self.__cfg.has_option(c_d.BLOCK_TRAN, c_d.SECT_PAIRS):
            pairs = self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS]

        tr_dict = {}
        if pairs:
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
            self.__cfg[department][c_d.OPTION_PREFIX] = prefix

            self.__write_cfg()
