import os

import global_vars as g_v
from logger_depr import *
from web_generator import html_defs as h_d

__all__ = ['HtmlGen']


class HtmlGen:
    def __init__(self, path, name):
        dir_p = g_v.OUT_PATH

        if not os.path.isabs(path):
            dir_p = os.path.join(dir_p, path)
        else:
            dir_p = path

        file_path = os.path.join(dir_p, name)

        if not os.path.exists(dir_p):
            os.mkdir(dir_p)

        self.file = open(file_path, 'w')

        if g_v.DEBUG: out_log("create file: " + file_path)

    def w_o_tag(self, tag, attr="", cr=False):
        self.file.write(h_d.TAG.format("", tag, attr))
        if cr:
            self.file.write(h_d.CR)
        self.file.flush()

    def w_txt(self, text):
        self.file.write(text)
        self.file.flush()

    def w_c_tag(self, tag):
        self.file.write(h_d.TAG.format(h_d.TAG_C, tag, ""))
        self.file.write(h_d.CR)
        self.file.flush()

    def w_tag(self, tag, text, attr="", cr=False):
        self.w_o_tag(tag, attr, cr)
        self.w_txt(text)
        self.w_c_tag(tag)


    def close(self):
        self.file.flush()
        self.file.close()