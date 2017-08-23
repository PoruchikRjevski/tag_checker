import os

import html_defs

DEF_DIR = "../out/"

class HtmlGen:
    def __init__(self, path, name):
        dir = os.path.dirname(os.path.realpath(__file__))

        if not path:
            dir = dir + "/" + DEF_DIR
        elif path:
            dir = dir + "/" + path

        if not os.path.isdir(dir):
            os.mkdir(dir, 0o777)

        self.file = open(dir + "/" + name, 'w')

    def writeTag(self, *args):
        if len(args) == 1:
            self.file.write(args[0])
        if len(args) == 2:
            self.file.write(args[0].format(args[1]))
        self.file.flush()

    def close(self):
        self.file.flush()
        self.file.close()