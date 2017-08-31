import datetime

import common
import html_defs

import js_scripts

from html_gen import HtmlGen
from tag_model import TagModel, Device, Note, Repo
from logger import out_log, out_err
from time_checker import TimeChecker


class WebGenerator:
    def __init__(self):
        out_log(self.__class__.__name__, "init")

    def generate_web(self, model):
        # create time checker
        timeCh = TimeChecker()
        out_log(self.__class__.__name__, "start gen web")

        timeCh.start

        # gen index
        self.gen_index(model)
        # cycle main
        self.genPages(model)
        timeCh.stop

        out_log(self.__class__.__name__, "finish gen web")
        out_log(self.__class__.__name__, timeCh.passed_time_str)

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
        self.gen_page_foot_info(main)
        self.genPageFoot(main)

        main.close()
        out_log(self.__class__.__name__, "finish gen main")

    def genMainContent(self, model, file):
        out_log(self.__class__.__name__, "gen main content")
        # deps = model.get_departments()
        deps = model.departments

        # for dep, repos in deps.items():
        for dep, repos in deps.items():
            firstDep = True
            allNotes = 0

            for repo in repos:
                for name, dev in repo.devices.items():
                    allNotes += len(dev.lastOrders)
                    out_log(self.__class__.__name__, "Notes for dev: " + name + " - " + str(allNotes))

            for repo in repos:
                for name, dev in repo.devices.items():
                    # generate device's own page
                    self.genOrdersPages(dep, dev, repo.link, repo.name)

                    # generate content for main page
                    firstDev = True
                    typeColor = common.TABLE_TR_COL_1

                    if not dev.lastOrders:
                        continue

                    curType = dev.lastOrders[0].type

                    for note in dev.lastOrders:
                        if curType != note.type:
                            curType = note.type
                            typeColor = self.decrement_color(typeColor)

                        file.write_tag(0, html_defs.T_TR_O,
                                       html_defs.A_ALIGN.format(common.ALIGN_C) +
                                       html_defs.A_BGCOLOR.format(common.TABLE_TR_COL_1))

                        if firstDep:
                            firstDep = False
                            self.genDepartment(file, dep, allNotes)

                        if firstDev:
                            firstDev = False
                            self.genDeviceName(file, dev.trName, len(dev.lastOrders), name)

                        self.genOrderNum(file,
                                         self.getNumByType(note.type, note.cnt),
                                         html_defs.A_TITLE.format(common.CNT_STR + str(dev.get_cnt_by_num(note.cnt)))
                                         + html_defs.A_BGCOLOR.format(typeColor),
                                         common.ORDERS_PATH + self.getOrderFileName(name, note.cnt))

                        self.genNoteDate(file, note.date,
                                         html_defs.A_TITLE.format(common.TAG_STR + note.tag)
                                         + html_defs.A_BGCOLOR.format(typeColor))

                        linkHash = note.pHash
                        if linkHash == -1:
                            linkHash = note.sHash

                        linkToRepo = common.LINK_TO_REPO.format(repo.name,
                                                                common.GW_SHORTLOG,
                                                                note.commMsg,
                                                                str(note.pHash))
                        self.genNoteHash(file,
                                         note.sHash,
                                         html_defs.A_BGCOLOR.format(typeColor),
                                         self.getTitleForCommit(repo.link,
                                                                note.author,
                                                                note.commDate,
                                                                note.commMsg),
                                         linkToRepo)

                        file.write_tag(0, html_defs.T_TR_C)

    def getTitleForCommit(self, repo, author, commDate, commMsg):
        return common.REPO_STR + repo + "\n" \
               + common.AUTHOR_STR + author + "\n" \
               + common.COMM_DATE_STR + commDate + "\n" \
               + common.COMM_MSG_SHORT.format(commMsg)

    def genDeviceName(self, file, name, span, link):
        out_log(self.__class__.__name__, "mapped name: " + name)
        self.genTd(file,
                   name,
                   html_defs.A_ROWSPAN.format(span))
        # self.genTd(file,
        #            name,
        #            html_defs.A_ROWSPAN.format(span),
        #            common.DEVICE_DIR + self.getDeviceFileName(link))

    def genOrderNum(self, file, num, attr, link):
        self.genTd(file, num, attr, link)

    def genDepartment(self, file, dep, nums):
        self.genTd(file, dep, html_defs.A_ROWSPAN.format(nums))

    def genNoteDate(self, file, date, attr):
        self.genTd(file,
                   str(date),
                   attr)

    def genNoteHash(self, file, hash, attr, title, link):
        self.genTd(file,
                   hash,
                   attr + html_defs.A_TITLE.format(title), link)

    def getNumByType(self, type, num):
        res = ""
        if common.TYPE_ALL in type:
            res = common.FOR_ALL
        elif common.TYPE_ITEM in type:
            res = common.ITEM_NUM + str(num)
        elif common.TYPE_ORDER in type:
            res = common.ORDER_NUM + str(num)
        return res

    def genOrdersPages(self, dep, device, repoLink, repoName):
        out_log(self.__class__.__name__, "start gen items pages for device: " + device.name)

        for key, val in device.orders.items():
            page = HtmlGen(common.ORDERS_PATH, self.getOrderFileName(device.name, val[0].cnt))

            self.genPageHead(page)
            self.genTableHead(page)
            self.gen_order_table_head(page,
                                      [common.HISTORY + device.trName + " - " + self.getNumByType(val[0].type,
                                                                                                  val[0].cnt),
                                      common.DEPART_STR + str(dep)])

            color = common.TABLE_TR_COL_1
            date = val[0].date
            for note in val:
                if date != note.date:
                    date = note.date
                    color = self.changeColor(color)

                page.write_tag(0, html_defs.T_TR_O,
                               html_defs.A_ALIGN.format(common.ALIGN_C) +
                               html_defs.A_BGCOLOR.format(color))

                self.genNoteDate(page,
                                 note.date,
                                 html_defs.A_TITLE.format(common.TAG_STR + note.tag)
                                 + html_defs.A_BGCOLOR.format(color))
                self.genNoteHash(page,
                                 note.sHash,
                                 html_defs.A_BGCOLOR.format(color),
                                 self.getTitleForCommit(repoLink,
                                                        note.author,
                                                        note.commDate,
                                                        note.commMsg),
                                 common.LINK_TO_REPO.format(repoName,
                                                            common.GW_SHORTLOG,
                                                            note.commMsg,
                                                            str(note.pHash)))

                page.write_tag(0, html_defs.T_TR_C)

            self.genTableFoot(page)
            self.genBackLink(page, common.LEVEL_UP + common.LEVEL_UP)
            self.gen_page_foot_info(page)
            self.genPageFoot(page)

            page.close()

        out_log(self.__class__.__name__, "finish gen items pages for device: " + device.name)

    def getDeviceFileName(self, name):
        return name + common.FILE_EXT

    def getOrderFileName(self, name, num):
        return name + "_" + str(num) + common.FILE_EXT

    def decrement_color(self, color):
        print(color[0])
        if color[0] == "#":
            color = color[1:]
        temp = int(color, 16)

        if temp >= common.COLOR_TOP_EDGE:
            temp = common.COLOR_BTM_EDGE
        else:
            temp -= common.COLOR_STEP
        return "#%06x" % temp

    def changeColor(self, color):
        if color == common.TABLE_TR_COL_1:
            color = common.TABLE_TR_COL_2
        elif color == common.TABLE_TR_COL_2:
            color = common.TABLE_TR_COL_1

        return color

    # 0 - gen, 1 - text, 2 - adding, 4 - link
    def genTd(self, *args):
        if len(args) < 2:
            return

        if len(args) >= 3:
            args[0].write_tag(0, html_defs.T_TD_O, args[2])
        else:
            args[0].write_tag(0, html_defs.T_TD_O)

        if len(args) == 4:
            args[0].write_tag(0, html_defs.T_A_O, html_defs.A_HREF.format(args[3]))

        args[0].write_tag(0, args[1])

        if len(args) == 4:
            args[0].write_tag(0, html_defs.T_A_C)

        args[0].write_tag(0, html_defs.T_TD_C)

    # 0 -gen, 1 - text, 2- adding
    def genFont(self, *args):
        if len(args) < 2:
            return

        if len(args) >= 3:
            args[0].write_tag(4, html_defs.T_FONT_O, args[2])
        else:
            args[0].write_tag(4, html_defs.T_FONT_O)

        args[0].write_tag(4, args[1])

        args[0].write_tag(4, html_defs.T_FONT_C)

    def genScript(self, gen, frameName):
        gen.write_tag(2, html_defs.T_SCRIPT_O,
                      html_defs.A_TYPE.format(html_defs.JS_SCRIPT))
        gen.write_tag(0, js_scripts.SCRIPTS.replace("%s", frameName))
        gen.write_tag(2, html_defs.T_SCRIPT_C)

    def genPageHead(self, gen):
        gen.write_tag(0, html_defs.HTML_HEAD)
        gen.write_tag(0, html_defs.T_HTML_O)
        gen.write_tag(1, html_defs.T_HEAD_O)
        gen.write_tag(2, html_defs.T_META_O, html_defs.A_CHARSET.format(common.DOC_CODE))
        gen.write_tag(1, html_defs.T_HEAD_C)
        gen.write_tag(1, html_defs.T_BODY_O, html_defs.A_LINK.format(common.BLACK) + html_defs.A_VLINK.format(common.BLACK))

    def genIFrameHead(self, gen):
        gen.write_tag(2, html_defs.T_IFRAME_O,
                      html_defs.A_ID.format(common.FRAME_ID) +
                      html_defs.A_STYLE.format(html_defs.A_ST_POS.format(common.FRAME_POS) +
                                              html_defs.A_ST_HEIGHT.format(common.FRAME_H) +
                                              html_defs.A_ST_WIDTH.format(common.FRAME_W) +
                                              html_defs.A_ST_BORDER.format(common.FRAME_BORDER)) +
                      html_defs.A_SRC.format(common.MAIN_NAME))

    def genIFrameFoot(self, gen):
        gen.write_tag(2, html_defs.T_IFRAME_C)

    def genTableHead(self, gen):
        gen.write_tag(2, html_defs.T_TABLE_O,
                      html_defs.A_BORDER.format(common.BORDER_WIDTH) +
                      html_defs.A_BGCOLOR.format(common.TABLE_COLOR) +
                      html_defs.A_CELLPADDING.format(common.CELLPADDING) +
                      html_defs.A_ALIGN.format(common.ALIGN_C) +
                      #html_defs.A_WIDTH.format(common.TABLE_WIDTH) +
                      html_defs.A_STYLE.format(html_defs.A_ST_FONT_FAM.format(common.FONT_FAM) +
                                              html_defs.A_ST_FONT_SZ.format(common.FONT_SZ)))

    def genTableFoot(self, gen):
        gen.write_tag(2, html_defs.T_TABLE_C)

    def gen_top_table_head(self, gen, attrList):
        gen.write_tag(3, html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.MAIN_T_HD_COL))  # TABLE_HD_COL
        gen.write_tag(4, html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MAIN_TABLE_COLS))

        for str in attrList:
            gen.write_tag(4, html_defs.T_H3_O)
            self.genFont(gen, str, html_defs.A_COLOR.format(common.WHITE))
            gen.write_tag(4, html_defs.T_H3_C)

        gen.write_tag(0, html_defs.T_TH_C)
        gen.write_tag(0, html_defs.T_TR_C)


    def genTopTableHead(self, gen, text):
        gen.write_tag(0, html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.MAIN_T_HD_COL)) #TABLE_HD_COL
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MAIN_TABLE_COLS))
        gen.write_tag(0, html_defs.T_H3_O)
        self.genFont(gen, text, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_H3_C)
        gen.write_tag(0, html_defs.T_H3_O)
        self.genFont(gen, text, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_H3_C)
        gen.write_tag(0, html_defs.T_TH_C)
        gen.write_tag(0, html_defs.T_TR_C)

    def genMidCommonTableBody(self, gen):
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.ITEM, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_TH_C)

    def genMidMainTableBody(self, gen):
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.DEPARTMENT, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_TH_C)
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.DEVICE, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_TH_C)

    def genMidTableHead(self, gen):
        gen.write_tag(0, html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))

    def genMidTableFoot(self, gen):
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.MID_ROWS))
        self.genFont(gen, common.LAST_SET, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_TH_C)
        gen.write_tag(0, html_defs.T_TR_C)

    def genBtmTableHead(self, gen):
        gen.write_tag(0, html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.TABLE_HD_COL))
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        self.genFont(gen, common.DATE, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.write_tag(0, html_defs.T_TH_O)
        self.genFont(gen, common.HASH_STR, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_TH_C, html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.write_tag(0, html_defs.T_TR_C)

    def genMainTableHead(self, gen):
        self.gen_top_table_head(gen, [common.MAIN_HEAD])
        self.genMidTableHead(gen)
        self.genMidMainTableBody(gen)
        self.genMidCommonTableBody(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def gen_device_table_head(self, *args):
        if len(args) < 2:
            return

        self.gen_top_table_head(args[0], args[1:])
        self.genMidTableHead(args[0])
        self.genMidCommonTableBody(args[0])
        self.genMidTableFoot(args[0])
        self.genBtmTableHead(args[0])


    def genDeviceTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.genMidTableHead(gen)
        self.genMidCommonTableBody(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def gen_order_table_head(self, gen, attrList):
        self.gen_top_table_head(gen, attrList)
        self.genMidTableHead(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genOrderTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.genMidTableHead(gen)
        self.genMidTableFoot(gen)
        self.genBtmTableHead(gen)

    def genBackLink(self, gen, levels):
        gen.write_tag(0, html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN_C))
        gen.write_tag(0, html_defs.T_A_O, html_defs.A_HREF.format(levels + common.MAIN_NAME))
        gen.write_tag(0, common.BACK)
        gen.write_tag(0, html_defs.T_A_C)
        gen.write_tag(0, html_defs.T_P_C)

    def gen_page_foot_info(self, gen):
        gen.write_tag(0, html_defs.T_P_O,
                      html_defs.A_ALIGN.format(common.ALIGN_C))
        gen.write_tag(0, html_defs.T_FONT_O,
                      html_defs.A_SIZE.format("2"))
        gen.write_tag(0, common.LAST_UPD + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        gen.write_tag(0, html_defs.T_FONT_C)
        gen.write_tag(0, html_defs.T_P_C)

        gen.write_tag(0, html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN_C))
        gen.write_tag(0, html_defs.T_FONT_O,
                      html_defs.A_SIZE.format("2"))
        gen.write_tag(0, common.COPYRIGHT)
        gen.write_tag(0, html_defs.T_FONT_C)
        gen.write_tag(0, html_defs.T_P_C)

    def genPageFoot(self, gen):
        gen.write_tag(1, html_defs.T_BODY_C)
        gen.write_tag(0, html_defs.T_HTML_C)