import os

import common
import html_defs

from html_gen import HtmlGen
from tag_model import TagModel
from logger import outLog
from logger import outErr

class WebGenerator:
    def generateWeb(self, model):
        outLog(self.__class__.__name__, "start gen web")

        index = HtmlGen(common.INDEX_PATH, common.INDEX_NAME)

        self.genPageHead(index)

        self.genTableHead(index)

        # self.genMainTableHead(index)
        self.genItemTableHead(index)

        self.genTableFoot(index)

        self.genBackLink(index)

        self.genPageFoot(index)

        index.close()

        outLog(self.__class__.__name__, "finish gen web")



    def genPageHead(self, gen):
        gen.writeTag(html_defs.T_HTML_O)
        gen.writeTag(html_defs.T_BODY_O)
        gen.writeTag(html_defs.T_META_O, html_defs.A_CHARSET.format(common.DOC_CODE))

    def genTableHead(self, gen):
        gen.writeTag(html_defs.T_TABLE_O,
                     html_defs.A_BORDER.format(common.BORDER_WIDTH) +
                     html_defs.A_BGCOLOR.format(common.TABLE_COLOR) +
                     html_defs.A_CELLPADDING.format(common.CELLPADDING) +
                     html_defs.A_WIDTH.format(common.TABLE_WIDTH) +
                     html_defs.A_STYLE.format(html_defs.A_ST_FONT_FAM.format(common.FONT_FAM) +
                                              html_defs.A_ST_FONT_SZ.format(common.FONT_SZ)))

    def genTableFoot(self, gen):
        gen.writeTag(html_defs.T_TABLE_C)

    def genTopTableHead(self, gen, text):
        gen.writeTag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.writeTag(html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MAIN_TABLE_COLS))
        gen.writeTag(html_defs.T_H3_O)
        gen.writeTag(text)
        gen.writeTag(html_defs.T_H3_C)
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TR_C)

    def genMidMainTableHead(self, gen):
        gen.writeTag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag("Отдел")
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag("Прибор")
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag("№")
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MID_ROWS))
        gen.writeTag("Последняя установка")
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TR_C)

    def genMidItemTableHead(self, gen):
        gen.writeTag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag("№")
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MID_ROWS))
        gen.writeTag("Последняя установка")
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TR_C)

    def genBtmTableHead(self, gen):
        gen.writeTag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.writeTag("Дата")
        gen.writeTag(html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.writeTag(html_defs.T_TH_O)
        gen.writeTag("Хэш-сумма")
        gen.writeTag(html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.writeTag(html_defs.T_TR_C)

    def genMainTableHead(self, gen):
        self.genTopTableHead(gen, "Актуальные прошивки")
        self.genMidMainTableHead(gen)
        self.genBtmTableHead(gen)

    def genItemTableHead(self, gen):
        self.genTopTableHead(gen, "ASW-1")
        self.genMidItemTableHead(gen)
        self.genBtmTableHead(gen)

    def genBackLink(self, gen):
        gen.writeTag(html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN))
        gen.writeTag(html_defs.T_A_O, html_defs.A_HREF.format(common.INDEX_NAME))
        gen.writeTag("Назад")
        gen.writeTag(html_defs.T_A_C)
        gen.writeTag(html_defs.T_P_C)

    def genPageFoot(self, gen):
        gen.writeTag(html_defs.T_BODY_C)
        gen.writeTag(html_defs.T_HTML_C)


    # -------------- OLD SHIT MAZAFAKA -----------------------
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
                        self.writeTd(dep, html_defs.SUPA % allTags)

                    if firstDev:
                        firstDev = False
                        self.writeTd(tag.itemName, html_defs.SUPA % len(repo.history))

                    self.writeTd(tag.itemNum, "")
                    self.writeTd(tag.orderNum, "")
                    self.writeTd(tag.date, "")
                    self.writeTd(tag.sHash, "")

                    self.writeCloseTr()

    def writeTd(self, field, supa):
        self.file.write(html_defs.TD_HD % supa)
        self.file.write(field)
        self.file.write(html_defs.TD_FT)

    def writeOpenTr(self):
        self.file.write(html_defs.TR_HD)

    def writeCloseTr(self):
        self.file.write(html_defs.TR_FT)

    def writeHead(self):
        outLog(self.__class__.__name__, "write head")
        self.file.write(html_defs.HEAD)

    def writeFoot(self):
        outLog(self.__class__.__name__, "write foot")
        self.file.write(html_defs.FOOT)

    