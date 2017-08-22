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

        self.file = open(common.INDEX_PATH + common.INDEX_NAME, 'w')

        if not self.file:
            outErr(self.__class__.__name__, "can't open file")
            return

        self.writeHead()

        self.writeMain(model)

        self.writeFoot()

        self.file.close()

    def writeMain(self, model):
        deps = model.getDepsKeys()
        for dep, repos in deps.items():
            firstDep = True
            allTags = 0
            for repo in repos:
                allTags = allTags + len(repo.history)

            for repo in repos:
                firstDev = True

                for tag in repo.history:
                    self.writeOpenTr()

                    if firstDep:
                        firstDep = False
                        self.writeTd(dep, web_gen_def.SUPA % allTags)

                    if firstDev:
                        firstDev = False
                        self.writeTd(tag.itemName, web_gen_def.SUPA % len(repo.history))

                    self.writeTd(tag.itemNum, "")
                    self.writeTd(tag.orderNum, "")
                    self.writeTd(tag.date, "")
                    self.writeTd(tag.sHash, "")

                    self.writeCloseTr()

    def writeTd(self, field, supa):
        self.file.write(web_gen_def.TD_HD % supa)
        self.file.write(field)
        self.file.write(web_gen_def.TD_FT)

    def writeOpenTr(self):
        self.file.write(web_gen_def.TR_HD)

    def writeCloseTr(self):
        self.file.write(web_gen_def.TR_FT)

    def writeHead(self):
        outLog(self.__class__.__name__, "write head")
        self.file.write(web_gen_def.HEAD)

    def writeFoot(self):
        outLog(self.__class__.__name__, "write foot")
        self.file.write(web_gen_def.FOOT)

    