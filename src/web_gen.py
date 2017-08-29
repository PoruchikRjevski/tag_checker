import datetime

import common
import html_defs

import js_scripts

from html_gen import HtmlGen
from tag_model import TagModel
from logger import out_log, out_err
from time_checker import TimeChecker


class WebGenerator:
    def __init__(self):
        out_log(self.__class__.__name__, "init")

    def generate_web(self, model):
        # create time checker
        timeCh = TimeChecker()
        out_log(self.__class__.__name__, "start gen web")

        timeCh.start()

        # gen index
        self.gen_index(model)
        # cycle main
        self.genPages(model)
        timeCh.stop()

        out_log(self.__class__.__name__, "finish gen web")
        out_log(self.__class__.__name__, timeCh.passed_time_str())

    def gen_index(self, model):
        out_log(self.__class__.__name__, "start gen index")
        index = HtmlGen(common.OUT_PATH, common.INDEX_NAME)

        self.genPageHead(index)

        self.genIFrameHead(index)
        # gen scripts
        self.genIFrameFoot(index)

        self.genScript(index, common.FRAME_ID)

        self.genPageFoot(index)

        index.close()
        out_log(self.__class__.__name__, "finish gen index")

    def genPages(self, model):
        out_log(self.__class__.__name__, "start gen main")
        main = HtmlGen(common.OUT_PATH, common.MAIN_NAME)

        self.genPageHead(main)
        self.genTableHead(main)

        self.genMainTableHead(main)

        self.genMainContent(model, main)

        self.genTableFoot(main)
        self.genPageFoot(main)

        main.close()
        out_log(self.__class__.__name__, "finish gen main")

    def genMainContent(self, model, file):
        out_log(self.__class__.__name__, "gen main content")
        deps = model.get_departments()

        # for dep, repos in deps.items():
        for dep, repos in deps.items():
            firstDep = True
            allNotes = 0

            for repo in repos:
                for name, dev in repo.get_devices().items():
                    allNotes += len(dev.get_last())

            for repo in repos:
                for name, dev in repo.get_devices().items():
                    # generate device's own page
                    self.genDevicePage(dev, repo.get_link())
                    self.genOrdersPages(dev, repo.get_link())

                    # generate content for main page
                    firstDev = True
                    firstType = True

                    if not dev.get_last():
                        continue
                    curType = dev.get_last()[0].type
                    rowsType = dev.get_last_num_by_type(curType)
                    for note in dev.get_last():
                        if curType != note.type:
                            firstType = True
                            curType = note.type
                            rowsType = dev.get_last_num_by_type(curType)

                        file.write_tag(html_defs.T_TR_O,
                                       html_defs.A_ALIGN.format(common.ALIGN) +
                                       html_defs.A_BGCOLOR.format(common.TABLE_TR_COL_1))

                        if firstDep:
                            firstDep = False
                            self.genDepartment(file, dep, allNotes)

                        if firstDev:
                            firstDev = False
                            self.genDeviceName(file, dev.get_mapped_name(), len(dev.get_last()), name)

                        self.genOrderNum(file,
                                         self.getNumByType(note.type, note.num),
                                         note.tag,
                                         common.ORDERS_PATH + self.getOrderFileName(name, note.num))

                        if firstType:
                            firstType = False
                            self.genNoteDate(file, note.date, rowsType)
                            self.genNoteHashWithCommDate(file,
                                                         note.sHash,
                                                         note.commDate,
                                                         rowsType,
                                                         self.getTitleForCommit(repo.get_link(), note.author))
                            # self.genNoteDate(file, note.date, len(dev.getLast()))
                            # self.genNoteHashWithCommDate(file, note.sHash, note.commDate, len(dev.getLast()))

                        file.write_tag(html_defs.T_TR_C)

    def getTitleForCommit(self, repo, author):
        return "Repo: " + repo + "\n" + "Author: " + author

    def genDeviceName(self, file, name, span, link):
        self.genTd(file,
                   name,
                   html_defs.A_ROWSPAN.format(span),
                   common.DEVICE_DIR + self.getDeviceFileName(link))

    def genOrderNum(self, file, num, tag, link):
        self.genTd(file, num, html_defs.A_TITLE.format(tag), link)

    def genDepartment(self, file, dep, nums):
        self.genTd(file, dep, html_defs.A_ROWSPAN.format(nums))

    def genNoteDate(self, file, date, nums):
        self.genTd(file,
                   str(date),
                   html_defs.A_ROWSPAN.format(nums))

    def genNoteHashWithCommDate(self, file, hash, commDate, nums, title):
        self.genTd(file,
                   hash + " (" + commDate + ")",
                   html_defs.A_ROWSPAN.format(nums) + html_defs.A_TITLE.format(title))

    def getNumByType(self, type, num):
        res = ""
        if common.TYPE_ALL in type:
            res = common.FOR_ALL
        elif common.TYPE_ITEM in type:
            res = common.ITEM_NUM + str(num)
        elif common.TYPE_ORDER in type:
            res = common.ORDER_NUM + str(num)
        return res

    def genDevicePage(self, device, repoLink):
        out_log(self.__class__.__name__, "start gen device page: " + device.get_name())
        page = HtmlGen(common.DEVICE_PATH, self.getDeviceFileName(device.get_name()))

        self.genPageHead(page)
        self.genTableHead(page)
        self.genDeviceTableHead(page, device.get_mapped_name())

        self.genDeviceContent(device, page, repoLink)

        self.genTableFoot(page)
        self.genBackLink(page, common.LEVEL_UP)
        self.genPageFoot(page)

        page.close()
        out_log(self.__class__.__name__, "finish gen device page: " + device.get_name())

    def genOrdersPages(self, device, repoLink):
        out_log(self.__class__.__name__, "start gen items pages for device: " + device.get_name())

        used = []

        for note in device.get_history():
            if not note.num in used:
                page = HtmlGen(common.ORDERS_PATH, self.getOrderFileName(device.get_name(), note.num))

                self.genPageHead(page)
                self.genTableHead(page)
                self.genOrderTableHead(page, device.get_mapped_name() + " - " + self.getNumByType(note.type, note.num))

                color = common.TABLE_TR_COL_1
                date = note.date
                for j in device.get_history():
                    if note.num == j.num:
                        if date != j.date:
                            date = j.date
                            color = self.changeColor(color)
                        page.write_tag(html_defs.T_TR_O,
                                       html_defs.A_ALIGN.format(common.ALIGN) +
                                       html_defs.A_BGCOLOR.format(color))

                        self.genNoteDate(page, j.date, common.BTM_ROWS)
                        self.genNoteHashWithCommDate(page,
                                                     j.sHash,
                                                     j.commDate,
                                                     common.BTM_ROWS,
                                                     self.getTitleForCommit(repoLink, j.author))

                        page.write_tag(html_defs.T_TR_C)

                self.genTableFoot(page)
                self.genBackLink(page, common.LEVEL_UP + common.LEVEL_UP)
                self.genPageFoot(page)

                page.close()

            used.append(note.num)

        out_log(self.__class__.__name__, "finish gen items pages for device: " + device.get_name())

    def getDeviceFileName(self, name):
        return name + common.FILE_EXT

    def getOrderFileName(self, name, num):
        return name + "_" + str(num) + common.FILE_EXT

    def changeColor(self, color):
        if color == common.TABLE_TR_COL_1:
            color = common.TABLE_TR_COL_2
        elif color == common.TABLE_TR_COL_2:
            color = common.TABLE_TR_COL_1

        return color

    def genDeviceContent(self, device, file, repoLink):
        out_log(self.__class__.__name__, "gen device content")
        date = device.get_history()[0].date
        color = common.TABLE_TR_COL_1

        firstDate = True
        notesByDate = 0

        for i in device.get_history():
            if i.date == date:
                notesByDate += 1

        for note in device.get_history():
            if date != note.date:
                notesByDate = 0
                firstDate = True
                date = note.date
                color = self.changeColor(color)

                for i in device.get_history():
                    if i.date == date:
                        notesByDate += 1

            file.write_tag(html_defs.T_TR_O,
                           html_defs.A_ALIGN.format(common.ALIGN) +
                           html_defs.A_BGCOLOR.format(color))

            self.genOrderNum(file,
                             self.getNumByType(note.type, note.num),
                             note.tag,
                             common.LEVEL_UP + common.ORDERS_PATH + self.getOrderFileName(device.get_name(), note.num))

            if firstDate:
                firstDate = False

                self.genNoteDate(file, note.date, notesByDate)
                self.genNoteHashWithCommDate(file,
                                             note.sHash,
                                             note.commDate,
                                             notesByDate,
                                             self.getTitleForCommit(repoLink, note.author))

            file.write_tag(html_defs.T_TR_C)

    # 0 - gen, 1 - text, 2 - adding, 4 - link
    def genTd(self, *args):
        if len(args) < 2:
            return

        if len(args) >= 3:
            args[0].write_tag(html_defs.T_TD_O, args[2])
        else:
            args[0].write_tag(html_defs.T_TD_O)

        if len(args) == 4:
            args[0].write_tag(html_defs.T_A_O, html_defs.A_HREF.format(args[3]))

        args[0].write_tag(args[1])

        if len(args) == 4:
            args[0].write_tag(html_defs.T_A_C)

        args[0].write_tag(html_defs.T_TD_C)

    # 0 -gen, 1 - text, 2- adding
    def genFont(self, *args):
        if len(args) < 2:
            return

        if len(args) >= 3:
            args[0].write_tag(html_defs.T_FONT_O, args[2])
        else:
            args[0].write_tag(html_defs.T_FONT_O)

        args[0].write_tag(args[1])

        args[0].write_tag(html_defs.T_FONT_C)

    def genScript(self, gen, frameName):
        gen.write_tag(html_defs.T_SCRIPT_O,
                      html_defs.A_TYPE.format(html_defs.JS_SCRIPT))
        gen.write_tag(js_scripts.SCRIPTS.replace("%s", frameName))
        gen.write_tag(html_defs.T_SCRIPT_C)

    def genPageHead(self, gen):
        gen.write_tag(html_defs.HTML_HEAD)
        gen.write_tag(html_defs.T_HTML_O)
        gen.write_tag(html_defs.T_HEAD_O)
        gen.write_tag(html_defs.T_META_O, html_defs.A_CHARSET.format(common.DOC_CODE))
        gen.write_tag(html_defs.T_HEAD_C)
        gen.write_tag(html_defs.T_BODY_O, html_defs.A_LINK.format(common.BLACK) + html_defs.A_VLINK.format(common.BLACK))

    def genIFrameHead(self, gen):
        gen.write_tag(html_defs.T_IFRAME_O,
                      html_defs.A_ID.format(common.FRAME_ID) +
                      html_defs.A_STYLE.format(html_defs.A_ST_POS.format(common.FRAME_POS) +
                                              html_defs.A_ST_HEIGHT.format(common.FRAME_H) +
                                              html_defs.A_ST_WIDTH.format(common.FRAME_W) +
                                              html_defs.A_ST_BORDER.format(common.FRAME_BORDER)) +
                      html_defs.A_SRC.format(common.OUT_PATH + common.MAIN_NAME))
        out_log(self.__class__.__name__, common.OUT_PATH + common.MAIN_NAME)

    def genIFrameFoot(self, gen):
        gen.write_tag(html_defs.T_IFRAME_C)

    def genTableHead(self, gen):
        gen.write_tag(html_defs.T_TABLE_O,
                      html_defs.A_BORDER.format(common.BORDER_WIDTH) +
                      html_defs.A_BGCOLOR.format(common.TABLE_COLOR) +
                      html_defs.A_CELLPADDING.format(common.CELLPADDING) +
                      html_defs.A_WIDTH.format(common.TABLE_WIDTH) +
                      html_defs.A_STYLE.format(html_defs.A_ST_FONT_FAM.format(common.FONT_FAM) +
                                              html_defs.A_ST_FONT_SZ.format(common.FONT_SZ)))

    def genTableFoot(self, gen):
        gen.write_tag(html_defs.T_TABLE_C)

    def genTopTableHead(self, gen, text):
        gen.write_tag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.MAIN_T_HD_COL)) #TABLE_HD_COL
        gen.write_tag(html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MAIN_TABLE_COLS))
        gen.write_tag(html_defs.T_H3_O)
        self.genFont(gen, text, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_H3_C)
        gen.write_tag(html_defs.T_TH_C)
        gen.write_tag(html_defs.T_TR_C)

    def genMidCommonTableBody(self, gen):
        gen.write_tag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.ITEM, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_TH_C)

    def genMidMainTableBody(self, gen):
        gen.write_tag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.DEPARTMENT, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_TH_C)
        gen.write_tag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.DEVICE, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_TH_C)

    def genMidTableHead(self, gen):
        gen.write_tag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))

    def genMidTableFoot(self, gen):
        gen.write_tag(html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.LAST_SET, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_TH_C)
        gen.write_tag(html_defs.T_TR_C)

    def genBtmTableHead(self, gen):
        gen.write_tag(html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.write_tag(html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        self.genFont(gen, common.DATE, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.write_tag(html_defs.T_TH_O)
        self.genFont(gen, common.HASH, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.write_tag(html_defs.T_TR_C)

    def genMainTableHead(self, gen):
        self.genTopTableHead(gen, common.MAIN_HEAD)
        self.genMidTableHead(gen)
        self.genMidMainTableBody(gen)
        self.genMidCommonTableBody(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genDeviceTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.genMidTableHead(gen)
        self.genMidCommonTableBody(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genOrderTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.genMidTableHead(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genBackLink(self, gen, levels):
        gen.write_tag(html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN))
        gen.write_tag(html_defs.T_A_O, html_defs.A_HREF.format(levels + common.MAIN_NAME))
        gen.write_tag(common.BACK)
        gen.write_tag(html_defs.T_A_C)
        gen.write_tag(html_defs.T_P_C)

    def genPageFoot(self, gen):
        gen.write_tag(html_defs.T_P_O,
                      html_defs.A_ALIGN.format(common.ALIGN))
        gen.write_tag(html_defs.T_FONT_O,
                      html_defs.A_SIZE.format("1"))
        gen.write_tag(common.LAST_UPD + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        gen.write_tag(html_defs.T_FONT_C)
        gen.write_tag(html_defs.T_P_C)

        gen.write_tag(html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN))
        gen.write_tag(html_defs.T_FONT_O,
                      html_defs.A_SIZE.format("1"))
        gen.write_tag(common.AUTHOR)
        gen.write_tag(html_defs.T_FONT_C)
        gen.write_tag(html_defs.T_P_C)

        gen.write_tag(html_defs.T_BODY_C)
        gen.write_tag(html_defs.T_HTML_C)