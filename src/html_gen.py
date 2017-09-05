import os

import common
from logger import out_log, out_err
import html_defs

DEF_DIR = "out/"

__all__ = ['HtmlGen']

class HtmlGen:
    def __init__(self, path, name):
        dir_p = common.OUT_PATH

        if not os.path.isabs(path):
               dir_p = os.path.join(dir_p, path)
        else:
            dir_p = path

        file_path = os.path.join(dir_p, name)
        out_log(self.__class__.__name__, "create file: " + file_path)

        self.file = open(file_path, 'w')

    def w_o_tag(self, tag, attr, cr=False):
        self.file.write(html_defs.TAG.format("", tag, attr))
        if cr:
            self.file.write(html_defs.CR)
        self.file.flush()

    def w_txt(self, text):
        self.file.write(text)
        self.file.flush()

    def w_c_tag(self, tag):
        self.file.write(html_defs.TAG.format(html_defs.TAG_C, tag, ""))
        self.file.write(html_defs.CR)
        self.file.flush()

    def w_tag(self, tag, text, attr, cr=False):
        self.w_o_tag(tag, attr, cr)
        self.w_txt(text)
        self.w_c_tag(tag)

    def close(self):
        self.file.flush()
        self.file.close()

    # old vision
    def write_tag(self, *args):
        if len(args) >= 1:
            for i in range(args[0]):
                self.file.write(html_defs.TAB_STR)
        if len(args) == 2:
            self.file.write(args[1].format(""))
        if len(args) == 3:
            self.file.write(args[1].format(args[2]))
        self.file.write(html_defs.NEXT_STR)
        self.file.flush()
