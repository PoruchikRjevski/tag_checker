import datetime

import common
import html_defs

from html_gen import HtmlGen
from tag_model import TagModel
from logger import outLog
from logger import outErr
from time_checker import TimeChecker

class WebGenerator:
    def generateWeb(self, model):
        # create time checker
        timeCh = TimeChecker()
        outLog(self.__class__.__name__, "start gen web")

        timeCh.start()
        # cycle main
        self.genPages(model)
        timeCh.stop()

        outLog(self.__class__.__name__, "finish gen web")
        outLog(self.__class__.__name__, timeCh.howMuchStr())


    def genPages(self, model):
        outLog(self.__class__.__name__, "start gen index")
        index = HtmlGen(common.INDEX_PATH, common.INDEX_NAME)

        self.genPageHead(index)
        self.genTableHead(index)

        self.genMainTableHead(index)

        self.genMainContent(model, index)

        self.genTableFoot(index)
        self.genPageFoot(index)

        index.close()
        outLog(self.__class__.__name__, "finish gen index")

    def genMainContent(self, model, file):
        outLog(self.__class__.__name__, "gen main content")
        deps = model.getDeps()

        # for dep, repos in deps.items():
        for dep, repos in deps.items():
            firstDep = True
            allNotes = 0

            for repo in repos:
                for name, dev in repo.getDevices().items():
                    allNotes += len(dev.getLast())

            for repo in repos:
                for name, dev in repo.getDevices().items():
                    # generate device's own page
                    self.genDevicePage(dev, name)

                    # generate content for main page
                    firstDev = True
                    firstType = True

                    if not dev.getLast():
                        continue
                    curType = dev.getLast()[0].type
                    rowsType = dev.getLastNumByType(curType)
                    for note in dev.getLast():
                        if curType != note.type:
                            firstType = True
                            curType = note.type
                            rowsType = dev.getLastNumByType(curType)

                        file.writeTag(html_defs.T_TR_O,
                                      html_defs.A_ALIGN.format(common.ALIGN) +
                                      html_defs.A_BGCOLOR.format(common.TABLE_TR_COL_1))

                        if firstDep:
                            firstDep = False
                            self.genDepartment(file, dep, allNotes)

                        if firstDev:
                            firstDev = False
                            self.genTd(file,
                                       note.name,
                                       html_defs.A_ROWSPAN.format(len(dev.getLast())),
                                       note.name)

                        self.genItemNum(file, self.getNumByType(note.type, note.num), note.tag)

                        if firstType:
                            firstType = False
                            self.genNoteDate(file, note.date, rowsType)
                            self.genNoteHashWithCommDate(file, note.sHash, note.commDate, rowsType)
                            # self.genNoteDate(file, note.date, len(dev.getLast()))
                            # self.genNoteHashWithCommDate(file, note.sHash, note.commDate, len(dev.getLast()))

                        file.writeTag(html_defs.T_TR_C)

    def genItemNum(self, file, num, tag):
        self.genTd(file, num, html_defs.A_TITLE.format(tag))

    def genDepartment(self, file, dep, nums):
        self.genTd(file, dep, html_defs.A_ROWSPAN.format(nums))

    def genNoteDate(self, file, date, nums):
        self.genTd(file,
                   str(date),
                   html_defs.A_ROWSPAN.format(nums))

    def genNoteHashWithCommDate(self, file, hash, commDate, nums):
        self.genTd(file,
                   hash + " (" + commDate + ")",
                   html_defs.A_ROWSPAN.format(nums))

    def getNumByType(self, type, num):
        res = ""
        if common.TYPE_ALL in type:
            res = common.FOR_ALL
        elif common.TYPE_ITEM in type:
            res = common.ITEM_NUM + str(num)
        elif common.TYPE_ORDER in type:
            res = common.ORDER_NUM + str(num)
        return res

    def genDevicePage(self, device, name):
        outLog(self.__class__.__name__, "start gen device page: " + name)
        page = HtmlGen(common.INDEX_PATH, name + common.FILE_EXT)

        self.genPageHead(page)
        self.genTableHead(page)
        self.genItemTableHead(page, name)

        self.genDeviceContent(device, page)

        self.genTableFoot(page)
        self.genBackLink(page)
        self.genPageFoot(page)

        page.close()
        outLog(self.__class__.__name__, "finish gen device page: " + name)

    def changeColor(self, color):
        if color == common.TABLE_TR_COL_1:
            color = common.TABLE_TR_COL_2
        elif color == common.TABLE_TR_COL_2:
            color = common.TABLE_TR_COL_1

        return color

    def genDeviceContent(self, device, file):
        outLog(self.__class__.__name__, "gen device content")
        date = device.getHistory()[0].date
        color = common.TABLE_TR_COL_1

        firstDate = True
        notesByDate = 0

        for i in device.getHistory():
            if i.date == date:
                notesByDate += 1

        for note in device.getHistory():
            if date != note.date:
                notesByDate = 0
                firstDate = True
                date = note.date
                color = self.changeColor(color)

                for i in device.getHistory():
                    if i.date == date:
                        notesByDate += 1

            file.writeTag(html_defs.T_TR_O,
                          html_defs.A_ALIGN.format(common.ALIGN) +
                          html_defs.A_BGCOLOR.format(color))

            self.genItemNum(file, self.getNumByType(note.type, note.num), note.tag)

            if firstDate:
                firstDate = False

                self.genNoteDate(file, note.date, notesByDate)
                self.genNoteHashWithCommDate(file, note.sHash, note.commDate, notesByDate)

            file.writeTag(html_defs.T_TR_C)

    # 0 - gen, 1 - text, 2 - adding, 4 - link
    def genTd(self, *args):
        if len(args) < 2:
            return

        if len(args) >= 3:
            args[0].writeTag(html_defs.T_TD_O, args[2])
        else:
            args[0].writeTag(html_defs.T_TD_O)

        if len(args) == 4:
            args[0].writeTag(html_defs.T_A_O, html_defs.A_HREF.format(args[3] + common.FILE_EXT))

        args[0].writeTag(args[1])

        if len(args) == 4:
            args[0].writeTag(html_defs.T_A_C)

        args[0].writeTag(html_defs.T_TD_C)

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

    def genMidCommonTableBody(self, gen):
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag(common.ITEM)
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MID_ROWS))
        gen.writeTag(common.LAST_SET)
        gen.writeTag(html_defs.T_TH_C)

    def genMidMainTableBody(self, gen):
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag(common.DEPARTMENT)
        gen.writeTag(html_defs.T_TH_C)
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.writeTag(common.DEVICE)
        gen.writeTag(html_defs.T_TH_C)

    def genMidTableHead(self, gen):
        gen.writeTag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))

    def genMidTableFoot(self, gen):
        gen.writeTag(html_defs.T_TR_C)

    def genBtmTableHead(self, gen):
        gen.writeTag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.writeTag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.writeTag(common.DATE)
        gen.writeTag(html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.writeTag(html_defs.T_TH_O)
        gen.writeTag(common.HASH)
        gen.writeTag(html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.writeTag(html_defs.T_TR_C)

    def genMainTableHead(self, gen):
        self.genTopTableHead(gen, common.MAIN_HEAD)
        self.genMidTableHead(gen)
        self.genMidMainTableBody(gen)
        self.genMidCommonTableBody(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genItemTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.genMidTableHead(gen)
        self.genMidCommonTableBody(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genBackLink(self, gen):
        gen.writeTag(html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN))
        gen.writeTag(html_defs.T_A_O, html_defs.A_HREF.format(common.INDEX_NAME))
        gen.writeTag(common.BACK)
        gen.writeTag(html_defs.T_A_C)
        gen.writeTag(html_defs.T_P_C)

    def genPageFoot(self, gen):
        gen.writeTag(html_defs.T_P_O,
                     html_defs.A_ALIGN.format(common.ALIGN))
        gen.writeTag(html_defs.T_FONT_O,
                     html_defs.A_SIZE.format("1"))
        gen.writeTag(common.LAST_UPD + datetime.datetime.now().strftime("%Y-%m-%d %I:%M"))
        gen.writeTag(html_defs.T_FONT_C)
        gen.writeTag(html_defs.T_P_C)

        gen.writeTag(html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN))
        gen.writeTag(html_defs.T_FONT_O,
                     html_defs.A_SIZE.format("1"))
        gen.writeTag(common.AUTHOR)
        gen.writeTag(html_defs.T_FONT_C)
        gen.writeTag(html_defs.T_P_C)

        gen.writeTag(html_defs.T_BODY_C)
        gen.writeTag(html_defs.T_HTML_C)