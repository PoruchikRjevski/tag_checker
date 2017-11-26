import os
import logging

import global_vars as g_v
import common_defs as c_d
from config_manager import dir_man
from web_generator import html_defs as h_d

__all__ = ['HtmlGen']


logger = logging.getLogger("{:s}.HtmlGen".format(c_d.SOLUTION))


class HtmlGen:
    def __init__(self, path, name):
        if not os.path.isabs(path):
            dir_p = os.path.join(dir_man.g_dir_man.output_dir, path)
        else:
            dir_p = path

        file_path = os.path.join(dir_p, name)

        if not os.path.exists(dir_p):
            os.makedirs(dir_p)

        self.file = open(file_path, 'w', encoding=c_d.DOC_ENCODING)

        logger.info("create file: " + file_path)

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