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

        # cycle main
        self.genPages(model)

        outLog(self.__class__.__name__, "finish gen web")


    def genPages(self, model):
        index = HtmlGen(common.INDEX_PATH, common.INDEX_NAME)

        self.genPageHead(index)
        self.genTableHead(index)

        self.genMainTableHead(index)

        self.genMainContent(model, index)

        self.genTableFoot(index)
        self.genPageFoot(index)

        index.close()

    def genMainContent(self, model, file):
        deps = model.getDepsKeys()
        for dep, repos in deps.items():
            firstDep = True
            allNotes = 0

            for repo in repos:
                for name, dev in repo.devices.items():
                    allNotes += len(dev.last)

            for repo in repos:
                for name, dev in repo.devices.items():
                    # generate device's own page
                    self.genDevicePage(dev, name)

                    # generate content for main page
                    firstDev = True
                    for note in dev.last:
                        file.writeTag(html_defs.T_TR_O,
                                      html_defs.A_ALIGN.format(common.ALIGN) +
                                      html_defs.A_BGCOLOR.format(common.TABLE_TR_COL))

                        if firstDep:
                            firstDep = False
                            self.genTd(file, dep, html_defs.A_ROWSPAN.format(allNotes))

                        if firstDev:
                            firstDev = False
                            file.writeTag(html_defs.T_TD_O, html_defs.A_ROWSPAN.format(len(dev.last)))
                            file.writeTag(html_defs.T_A_O, html_defs.A_HREF.format(note.name + common.FILE_EXT))
                            file.writeTag(note.name)
                            file.writeTag(html_defs.T_A_C)
                            file.writeTag(html_defs.T_TD_C)

                        if common.TYPE_ALL in note.type:
                            self.genTd(file, "для всех")
                        elif common.TYPE_ITEM in note.type:
                            self.genTd(file, "Зав. № " + str(note.num))
                        elif common.TYPE_ORDER in note.type:
                            self.genTd(file, "Заказ  " + str(note.num))

                        self.genTd(file, str(note.date))
                        self.genTd(file, note.sHash + "(" + note.commDate + ")")

                        file.writeTag(html_defs.T_TR_C)

    def genDevicePage(self, device, name):
        page = HtmlGen(common.INDEX_PATH, name + common.FILE_EXT)

        self.genPageHead(page)
        self.genTableHead(page)
        self.genItemTableHead(page, name)

        self.genDeviceContent(device, page)

        self.genTableFoot(page)
        self.genBackLink(page)
        self.genPageFoot(page)

        page.close()

    def genDeviceContent(self, device, file):
        for note in device.history:
            file.writeTag(html_defs.T_TR_O,
                          html_defs.A_ALIGN.format(common.ALIGN) +
                          html_defs.A_BGCOLOR.format(common.TABLE_TR_COL))

            if common.TYPE_ALL in note.type:
                self.genTd(file, "для всех")
            elif common.TYPE_ITEM in note.type:
                self.genTd(file, "Зав. № " + str(note.num))
            elif common.TYPE_ORDER in note.type:
                self.genTd(file, "Заказ  " + str(note.num))

            self.genTd(file, str(note.date))
            self.genTd(file, note.sHash + "(" + note.commDate + ")")

            file.writeTag(html_defs.T_TR_C)

    # 0 - gen, 1 - text, 2 - adding
    def genTd(self, *args):
        if len(args) < 2:
            return

        if len(args) == 3:
            args[0].writeTag(html_defs.T_TD_O, args[2])
        else:
            args[0].writeTag(html_defs.T_TD_O)

        args[0].writeTag(args[1])
        args[0].writeTag(html_defs.T_TH_C)

    def genPageHead(self, gen):
        gen.writeTag(html_defs.HTML_HEAD)
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

    def genItemTableHead(self, gen, text):
        self.genTopTableHead(gen, "История установки прошивок для устойства: " + text)
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


# -------------- OLD SHIT MAZAFAKA --------------------------------------------
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

    