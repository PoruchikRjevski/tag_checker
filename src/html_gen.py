import os

import common
from logger import out_log, out_err
import html_defs

DEF_DIR = "out/"


class HtmlGen:
    def __init__(self, path, name):
        dir = common.OUT_PATH

        if not os.path.isabs(path):
               dir = dir + path
        else:
            dir = path

        #if not os.path.isdir(dir):
        #    os.makedirs(dir, 0o777)

        filePath = dir + name
        out_log(self.__class__.__name__, "create file: " + filePath)

        self.file = open(filePath, 'w')

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

    def close(self):
        self.file.flush()
        self.file.close()