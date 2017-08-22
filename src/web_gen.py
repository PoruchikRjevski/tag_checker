import os

import common
import web_gen_def

from tag_model import TagModel
from logger import outLog
from logger import outErr

class WebGenerator:
    def generateIndex(self, model):
        outLog(self.__class__.__name__, "start gen index")

        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        if not os.path.isdir(common.INDEX_PATH):
            outLog(self.__class__.__name__, "make dir: " + common.INDEX_PATH)
            os.mkdir(common.INDEX_PATH, 0o777)

        indexF = open(common.INDEX_PATH + common.INDEX_NAME, 'w')

        if not indexF:
            outErr(self.__class__.__name__, "can't open file")
            return

        self.writeHead(indexF)
        self.writeFoot(indexF)

        indexF.close()

    def writeHead(self, file):
        outLog(self.__class__.__name__, "write head")
        file.write(web_gen_def.HEAD)

    def writeFoot(self, file):
        outLog(self.__class__.__name__, "write foot")
        file.write(web_gen_def.FOOT)

    