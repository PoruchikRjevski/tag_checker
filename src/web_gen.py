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

        self.writeMain(model, indexF)

        self.writeFoot(indexF)

        indexF.close()

    def writeMain(self, model, file):
        deps = model.getDepsKeys()
        for dep, repos in deps.items():
            firstDep = True
            allTags = 0
            for repo in repos:
                allTags = allTags + len(repo.history)

            for repo in repos:
                firstDev = True
                for tag in repo.history:
                    self.writeOpenTr(file)

                    if firstDep:
                        firstDep = False
                        self.writeTd(file, dep, web_gen_def.SUPA % allTags)

                    if firstDev:
                        firstDev = False
                        self.writeTd(file, tag.itemName, web_gen_def.SUPA % len(repo.history))

                    self.writeTd(file, tag.itemNum, "")
                    self.writeTd(file, tag.orderNum, "")
                    self.writeTd(file, tag.date, "")
                    self.writeTd(file, tag.sHash, "")

                    self.writeCloseTr(file)

    def writeTd(self, file, field, supa):
        file.write(web_gen_def.TD_HD % supa)
        file.write(field)
        file.write(web_gen_def.TD_FT)

    def writeOpenTr(self, file):
        file.write(web_gen_def.TR_HD)

    def writeCloseTr(self, file):
        file.write(web_gen_def.TR_FT)


    def writeHead(self, file):
        outLog(self.__class__.__name__, "write head")
        file.write(web_gen_def.HEAD)

    def writeFoot(self, file):
        outLog(self.__class__.__name__, "write foot")
        file.write(web_gen_def.FOOT)

    