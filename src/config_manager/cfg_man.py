import os
import sys
import configparser
import logging

import common_defs as c_d
import global_vars as g_v
from tag_model import *
from cmd_executor.cmd_executor import *
from logger import log_func_name

__all__ = ['CfgLoader']


logger = logging.getLogger("{:s}.CfgLoader".format(c_d.SOLUTION))


# TODO: maybe json will be simpler?

class CfgLoader:
    def __init__(self, updates_list = None):
        if updates_list is None:
            updates_list = []

        logging.info("{:s} init".format(CfgLoader.__name__))

        self.__partly_update = False
        self.__update_list = updates_list

        self.__cfg = None
        self.__gen_paths()
        CfgLoader.__set_default_out_path()

        res = self.open_cfg()
        if not res is None:
            sys.exit(res)

    @property
    def partly_update(self):
        return self.__partly_update

    @partly_update.setter
    def partly_update(self, flag):
        self.__partly_update = flag

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

    @log_func_name(logger)
    def __load_config_block(self, block):
        g_v.OUT_PATH = self.__try_load(block, c_d.OUT_P, g_v.OUT_PATH)
        g_v.DIST_LINK_PREFIX = self.__try_load(block, c_d.SECT_DIST_LINK_PREFIX, g_v.DIST_LINK_PREFIX)
        g_v.DIST_LINK_PATTERN = self.__try_load(block, c_d.SECT_DIST_LINK_PATTERN, g_v.DIST_LINK_PATTERN)

    @log_func_name(logger)
    def __load_translate_block(self, block, model):
        if self.__cfg.has_option(block, c_d.SECT_PAIRS):
            pairs = self.__cfg.get(block, c_d.SECT_PAIRS)
            tr_dict = dict(item.split(":") for item in pairs.split("|") if item)

            model.tr_dev_names.update(tr_dict)

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

    @log_func_name(logger)
    def __add_department(self, block, model):
        prefix = self.__get_dep_prefix(block)

        repos_links = self.__cfg.get(block, c_d.OPTION_REPOS).split("\n")

        if repos_links:
            dep = Department(block)

            split = []
            pre_link = ""

            for repo_name in repos_links:
                if not repo_name:
                    continue

                repo_obj = Repo()

                split = repo_name.split(":")
                item_count = len(split)
                sw_archive_module_id = ""
                sw_archive_module_group_id = ""

                if isinstance(split, list) and item_count > 1:
                    repo_obj.soft_type = split[0]

                    if repo_obj.soft_type not in dep.soft_types:
                        dep.soft_types.append(repo_obj.soft_type)

                    pre_link = split[1]

                    if item_count > 2:
                        sw_archive_module_group_id = split[2]
                    if item_count > 3:
                        sw_archive_module_id = split[3]
                else:
                    pre_link = repo_name

                repo_obj.link = prefix + pre_link
                repo_obj.name = pre_link
                
                if not sw_archive_module_id:
                    repo_obj.sw_archive_module_id = CfgLoader.get_sw_module_id_from_repo_full_link(repo_obj.link)
                else:
                    repo_obj.sw_archive_module_id = sw_archive_module_id

                if not sw_archive_module_group_id:
                    sw_archive_module_group_id = CfgLoader.get_sw_module_group_id_from_repo_full_link(repo_obj.link)

                if len(sw_archive_module_group_id) > 0:
                    sw_archive_module_group_id = sw_archive_module_group_id + "/"
                
                repo_obj.sw_archive_module_group_id = sw_archive_module_group_id

                update_repo_flag = True

                if self.__partly_update:
                    if pre_link not in self.__update_list:
                        update_repo_flag = False

                dep.repos.append({UPDATE_FLAG: update_repo_flag, REPO_OBJECT: repo_obj})

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
            return c_d.EXIT_CFNE

        self.__cfg = configparser.ConfigParser()
        self.__cfg.read(self.__config_def_path)

        return None

    @staticmethod
    def __rewrite_update_file(cfg_parser, repos):
        cfg_parser[c_d.SECTION_UPD][c_d.OPTION_UPD] = repos

        with open(c_d.UPDATE_TABLE_PATH, 'w') as file:
            cfg_parser.write(file)

            file.flush()
            file.close()

            logger.info("update.ini was rewrited.")

    @staticmethod
    def get_list_of_updates():
        cfg_parser = configparser.ConfigParser()

        cfg_parser.read(c_d.UPDATE_TABLE_PATH)

        repos = None

        if not cfg_parser.has_section(c_d.SECTION_UPD):
            cfg_parser[c_d.SECTION_UPD] = {}

        if cfg_parser.has_option(c_d.SECTION_UPD, c_d.OPTION_UPD):
            repos = cfg_parser[c_d.SECTION_UPD][c_d.OPTION_UPD]

        if not repos is None:
            res = repos.split("\n")
            res = [repo for repo in res if repo]

            CfgLoader.__rewrite_update_file(cfg_parser, "")

            return res

        return []

    @staticmethod
    def add_repo_to_updates(repo_name):
        logger.info("try add repo {:s} to updates.ini".format(str(repo_name)))
        cfg_parser = configparser.ConfigParser()

        cfg_parser.read(c_d.UPDATE_TABLE_PATH)

        repos = None

        if not cfg_parser.has_section(c_d.SECTION_UPD):
            cfg_parser[c_d.SECTION_UPD] = {}

        if cfg_parser.has_option(c_d.SECTION_UPD, c_d.OPTION_UPD):
            repos = cfg_parser[c_d.SECTION_UPD][c_d.OPTION_UPD]

        if repos is None:
            repos = repo_name
        else:
            repos_splitted = repos.split("\n")
            if repo_name not in repos_splitted:
                repos_splitted.append(repo_name)

                repos = "\n".join(repos_splitted)

        logger.info("Now repos in updates.ini: {:s}".format(repos))

        CfgLoader.__rewrite_update_file(cfg_parser, repos)

    @staticmethod
    def __rem_repo_from_updates(repo_name):
        logger.info("try del repo {:s} from updates.ini".format(str(repo_name)))
        cfg_parser = configparser.ConfigParser()

        cfg_parser.read(c_d.UPDATE_TABLE_PATH)

        repos = None

        if not cfg_parser.has_section(c_d.SECTION_UPD):
            cfg_parser[c_d.SECTION_UPD] = {}

        if cfg_parser.has_option(c_d.SECTION_UPD, c_d.OPTION_UPD):
            repos = cfg_parser[c_d.SECTION_UPD][c_d.OPTION_UPD]

        if not repos is None:
            repos_splitted = repos.split("\n")

            if repo_name in repos_splitted:
                repos_splitted.remove(repo_name)

            repos = "\n".join(repos_splitted)

            CfgLoader.__rewrite_update_file(cfg_parser, repos)

        logger.info("Now repos in updates.ini: {:s}".format(repos))


    @log_func_name(logger)
    def load_config(self, model):
        blocks = self.__cfg.sections()

        for block in blocks:
            if block == c_d.BLOCK_CONFIG:
                self.__load_config_block(block)
            elif block == c_d.BLOCK_TRAN:
                self.__load_translate_block(block, model)
            else:
                self.__add_department(block, model)

        return True

    def show(self, block=""):
        if block:
            logger.info("Reques to show {:s}".format(block))
        else:
            logger.info("Reques to show departments")

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

    @staticmethod
    def __do_add_hook(src, dst):
        run_cmd("yes | cp -rf {:s} {:s}".format(src, dst))

    @staticmethod
    def __do_rem_hook(dst):
        run_cmd("rm -f {:s}".format(dst))

    def __add_git_hooks(self, dep, repo):
        logger.info("try to add githook to {:s} of {:s}".format(repo,
                                                                dep))
        _, repo = self.__separate_repo_and_soft_type(repo)

        hooks_path = os.path.join(c_d.GIT_HOOKS_PATH, c_d.POST_RX_HOOK_NAME)

        repo_path = self.__get_repo_path(dep, repo)
        repo_hooks_dir_path = os.path.join(repo_path, c_d.HOOKS_PATH)

        self.__do_add_hook(hooks_path, repo_hooks_dir_path)

    def __rem_git_hooks(self, dep, repo):
        logger.info("try to del githook from {:s} of {:s}".format(repo,
                                                                dep))
        _, repo = self.__separate_repo_and_soft_type(repo)

        repo_path = self.__get_repo_path(dep, repo)
        hook_path = os.path.join(repo_path, c_d.HOOKS_PATH, c_d.POST_RX_HOOK_NAME)

        self.__do_rem_hook(hook_path)

    @staticmethod
    def setup_hooks(tag_model):
        hook_path = os.path.join(c_d.GIT_HOOKS_PATH, c_d.POST_RX_HOOK_NAME)

        for dep_name, dep_obj in tag_model.departments.items():
            for repo in dep_obj.repos:
                repo_obj = repo[REPO_OBJECT]

                if os.path.exists(repo_obj.link):
                    dst = os.path.join(repo_obj.link, c_d.HOOKS_PATH)

                    CfgLoader.__do_add_hook(hook_path, dst)

    def add_repo(self, block, repos):
        if not block or not repos:
            return

        logger.info("try to add {:s} to {:s}".format(" ".join(repos) if isinstance(repos, list) else repos,
                                                     block))

        repos_b = ""

        if self.__cfg.has_section(block):
            if self.__cfg.has_option(block, c_d.OPTION_REPOS):
                repos_b = self.__cfg[block][c_d.OPTION_REPOS] + "\n"
        else:
            self.__cfg[block] = {c_d.OPTION_PREFIX : "", c_d.OPTION_REPOS : ""}

        if isinstance(repos, list):
            for repo in repos:
                repos_b += "{:s}\n".format(repo)

                self.__add_git_hooks(block, repo)
                self.add_repo_to_updates(repo)
        else:
            repos_b += "{:s}\n".format(repos)
            self.__add_git_hooks(block, repos)
            self.add_repo_to_updates(repos)

        self.__cfg[block][c_d.OPTION_REPOS] = repos_b

        self.__write_cfg()

    def rem_repo(self, block, repos):
        if not block or not repos:
            return

        logger.info("try to del {:s} from {:s}".format(" ".join(repos) if isinstance(repos, list) else repos,
                                                     block))

        repos_b = ""

        if self.__cfg.has_section(block):
            if self.__cfg.has_option(block, c_d.OPTION_REPOS):
                repos_b = self.__cfg[block][c_d.OPTION_REPOS]

                if isinstance(repos, list):
                    for repo in repos:
                        repos_b = repos_b.replace(repo, "").rstrip().lstrip()
                        self.__rem_git_hooks(block, repo)
                        self.__rem_repo_from_updates(repo)
                else:
                    repos_b = repos_b.replace(repos, "").rstrip().lstrip()
                    self.__rem_git_hooks(block, repos)
                    self.__rem_repo_from_updates(repos)

                self.__cfg[block][c_d.OPTION_REPOS] = repos_b

                self.__write_cfg()

    def add_translate(self, name, tr_name):
        logger.info("try to add tr {:s} for {:s}".format(tr_name, name))
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

        logger.info("now translates: {:s}".format(pairs))

        self.__cfg[c_d.BLOCK_TRAN][c_d.SECT_PAIRS] = pairs

        self.__write_cfg()

    def rem_translate(self, translates):
        logger.info("try to rem tr for {:s}".format(" ".join(translates) if isinstance(translates, list) else translates))
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

                logger.info("now translates: {:s}".format(pairs))

    def add_department(self, deps):
        logger.info("try to add departments {:s}".format(" ".join(deps) if isinstance(deps, list) else deps))
        if isinstance(deps, list):
            for dep in deps:
                if not self.__cfg.has_section(dep):
                    self.__cfg[dep] = {}
        else:
            self.__cfg[deps] = {}

        self.__write_cfg()

    def rem_department(self, deps):
        logger.info("try to del departments {:s}".format(" ".join(deps) if isinstance(deps, list) else deps))
        if isinstance(deps, list):
            for dep in deps:
                if self.__cfg.has_section(dep):
                    del self.__cfg[dep]
        else:
            del self.__cfg[deps]

        self.__write_cfg()

    def change_prefix(self, dep, prefix):
        logger.info("try to change prefix {:s} in dep {:s}".format(prefix, dep))
        if self.__cfg.has_section(dep):
            self.__cfg[dep][c_d.OPTION_PREFIX] = prefix

            self.__write_cfg()
