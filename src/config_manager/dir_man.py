import sys

import os

import common_defs as c_d


class DirManager:

    def __init__(self):
        self.root_dir = ""
        self.logger_dir = ""
        self.config_dir = ""
        self.config_file_path = ""
        self.output_dir = ""
        self.bin_dir = ""
        self.git_hooks_dir = ""
        self.update_table_file_path = ""
        self.data_dir = ""
        self.output_device_dir = ""
        self.output_orders_dir = ""

        self.def_root_dir = os.getcwd()
        self.def_bin_dir = "bin/"
        self.def_config_dir = "etc/"
        self.def_data_dir = "usr/shared/"
        self.def_output_dir = "var/www/"
        self.def_logger_dir = "var/log/"

        self.configure_by_platform()

    def configure_by_platform(self, platform = ""):
        if not platform:
            platform = sys.platform

        if platform == c_d.WINDOWS_P:
            self.default_configure_for_win()
        else:
            self.default_configure_for_unix()

    def reconfigure(self, root_dir = ""):
        if root_dir:
            self.root_dir = root_dir

        if not self.root_dir:
            self.root_dir = self.def_root_dir

        if not os.path.isabs(self.root_dir):
            self.root_dir = os.path.join(os.getcwd(), self.root_dir)

        self.logger_dir = self.abs_path(self.def_logger_dir)
        self.config_dir = self.abs_path(self.def_config_dir)
        self.bin_dir = self.abs_path(self.def_bin_dir)
        self.data_dir = self.abs_path(self.def_data_dir)
        self.git_hooks_dir = os.path.join(self.data_dir, c_d.GIT_HOOKS_PATH)

        self.config_file_path = os.path.join(self.config_dir, c_d.CONFIG_FILE_NAME)
        self.update_table_file_path = os.path.join(self.config_dir, c_d.UPDATE_TABLE_FILE_NAME)

        self.output_dir = self.abs_path(self.def_output_dir)
        self.output_device_dir = os.path.join(self.output_dir, c_d.OUTPUT_DEVICE_REL_DIR)
        self.output_orders_dir = os.path.join(self.output_device_dir, c_d.OUTPUT_DEVICE_ORDERS_REL_DIR)

    def abs_path(self, path):
        if os.path.isabs(path):
            return path
        else:
            return os.path.join(self.root_dir, path)

    def default_configure_short_rel_paths(self, root_dir = ""):
        if root_dir:
            self.def_root_dir = root_dir
        self.def_logger_dir = "log"
        self.def_config_dir = "cfg"
        self.def_bin_dir = "bin"
        self.def_data_dir = "data"
        self.def_output_dir = "www"
        self.reconfigure()

    def default_configure_long_rel_paths(self, name = "tag_checker", root_dir = ""):
        if root_dir:
            self.def_root_dir = root_dir
        self.def_logger_dir = os.path.join("tmp", name, "log")
        self.def_config_dir = os.path.join("etc", name)
        self.def_bin_dir = os.path.join("opt", name)
        self.def_data_dir = os.path.join("opt", name)
        self.def_output_dir = os.path.join("var", "www", "swver_hist")
        self.reconfigure()

    def default_configure_for_in_project_run(self):
        self.default_configure_short_rel_paths(os.path.join(os.getcwd(), "..", ".work", "root"))

    def default_configure_for_win(self):
        self.default_configure_short_rel_paths("C:\\opt\\tag_checker")

    def default_configure_for_unix(self):
        self.default_configure_long_rel_paths("tag_checker", "/")


g_dir_man = DirManager()
g_dir_man.reconfigure()