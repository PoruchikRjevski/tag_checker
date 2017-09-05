import datetime
import os

import common
import html_defs

from html_gen import HtmlGen
from tag_model import TagModel, Device, Note, Repo
from logger import out_log, out_err
from time_checker import TimeChecker


class WebGenerator:
    def __init__(self):
        out_log(self.__class__.__name__, "init")

    def __join_paths(self, first, sec):
        return os.path.join(first, sec)

    def __gen_index(self, model):
        out_log(self.__class__.__name__, "start gen index")
        index = HtmlGen(common.OUT_PATH, common.INDEX_F_NAME)

        self.__gen_page_head(index)
        self.__gen_iframe(index)
        self.__gen_script(index, common.FRAME_ID)
        self.__gen_page_foot(index)

        index.close()
        out_log(self.__class__.__name__, "finish gen index")

    def __gen_pages(self, model):
        out_log(self.__class__.__name__, "start gen main")
        main = HtmlGen(common.OUT_PATH, common.MAIN_F_NAME)

        self.__gen_page_head(main)
        self.__gen_table_head(main)

        self.__gen_main_table_head(main)

        self.__gen_main_content(model, main)

        self.__gen_table_foot(main)
        self.__gen_page_foot_info(main)
        self.__gen_page_foot(main)

        main.close()
        out_log(self.__class__.__name__, "finish gen main")

    def __gen_page_head(self, gen):
        gen.w_o_tag(html_defs.T_HTML, "", True)
        gen.w_o_tag(html_defs.T_HEAD, "", True)
        gen.w_o_tag(html_defs.T_META, html_defs.A_CHARSET.format(common.DOC_CODE), True)
        gen.w_o_tag(html_defs.T_LINK,
                    html_defs.A_REL.format(html_defs.A_REL_SS)
                    + html_defs.A_HREF.format(common.STYLE_F_NAME), True)
        gen.w_c_tag(html_defs.T_HEAD)
        gen.w_o_tag(html_defs.T_BODY, "", True)

    def __gen_page_foot(self, gen):
        gen.w_c_tag(html_defs.T_BODY)
        gen.w_c_tag(html_defs.T_HTML)

    def __gen_iframe(self, gen):
        gen.w_tag(html_defs.T_IFRAME,
                  common.FRAME_NOT,
                  html_defs.A_ID.format(common.FRAME_ID) +
                  html_defs.A_STYLE.format(html_defs.A_ST_POS.format(common.FRAME_POS) +
                                           html_defs.A_ST_H.format(common.FRAME_H) +
                                           html_defs.A_ST_W.format(common.FRAME_W) +
                                           html_defs.A_ST_BORDER.format(common.FRAME_BORDER)) +
                  html_defs.A_SRC.format(common.MAIN_F_NAME))

    def __gen_script(self, gen, frame_name):
        gen.w_tag(html_defs.T_SCRIPT,
                  "",
                  html_defs.A_TYPE.format(html_defs.A_T_JS) +
                  html_defs.A_SRC.format(common.SCRIPTS_F_NAME))

    def __gen_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TABLE,
                    html_defs.A_CLASS.format(common.CL_MAIN_TABLE),
                    True)

    def __gen_table_foot(self, gen):
        gen.w_c_tag(html_defs.T_TABLE)

    def __gen_page_foot_info(self, gen):
        gen.w_tag(html_defs.T_P,
                  common.LAST_UPD_TXT + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                  html_defs.A_CLASS.format(common.CL_FOOT_INFO))
        gen.w_tag(html_defs.T_P,
                  common.CR_TXT,
                  html_defs.A_CLASS.format(common.CL_FOOT_INFO))

    def __gen_main_table_head(self, gen):
        self.__gen_top_main_table_head(gen)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_main_table_body(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_main_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common.CL_MT_H),
                    True)
        gen.w_o_tag(html_defs.T_TH,
                    html_defs.A_COLSPAN.format(common.M_TABLE_COLSPAN),
                    True)

        gen.w_o_tag(html_defs.T_H.format(common.M_TABLE_H_NUM),
                    "")
        gen.w_txt(common.M_HEAD_TXT)
        gen.w_c_tag(html_defs.T_H.format(common.M_TABLE_H_NUM))

        gen.w_c_tag(html_defs.T_TH)
        gen.w_c_tag(html_defs.T_TR)

    def __gen_mid_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common.CL_MT_F),
                    True)

    def __gen_mid_main_table_body(self, gen):
        gen.w_tag(html_defs.T_TH,
                  common.DEP_TXT,
                  html_defs.A_ROWSPAN.format(common.MID_ROWS))
        gen.w_tag(html_defs.T_TH,
                  common.DEV_TXT,
                  html_defs.A_ROWSPAN.format(common.MID_ROWS))

    def __gen_mid_common_table_body(self, gen):
        gen.w_tag(html_defs.T_TH,
                  common.ITEM_TXT,
                  html_defs.A_ROWSPAN.format(common.MID_ROWS))

    def __gen_mid_table_foot(self, gen):
        gen.w_tag(html_defs.T_TH,
                  common.LAST_SET_TXT,
                  html_defs.A_COLSPAN.format(common.MID_ROWS))
        gen.w_c_tag(html_defs.T_TR)

    def __gen_bottom_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common.CL_MT_F),
                    True)
        gen.w_tag(html_defs.T_TH,
                  common.DATE_TXT,
                  html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.w_tag(html_defs.T_TH,
                  common.HASH_TXT,
                  html_defs.A_ROWSPAN.format(common.BTM_ROWS))
        gen.w_c_tag(html_defs.T_TR)

    def __gen_main_content(self, model, file):
        out_log(self.__class__.__name__, "start gen main content")

        deps = model.departments

        for dep, repos in deps.items():
            first_dep = True
            all_notes = 0

            for repo in repos:
                for name, dev in repo.devices.items():
                    all_notes += len(dev.lastOrders)
                    out_log(self.__class__.__name__, "Notes for dev: " + name + " - " + str(all_notes))

            for repo in repos:
                for name, dev in repo.devices.items():
                    # generate device's own page
                    # self.genOrdersPages(dep, dev, repo.link, repo.name)

                    # generate content for main page
                    first_dev = True
                    type_class_id = 0

                    if not dev.lastOrders:
                        continue

                    cur_type = dev.lastOrders[0].type

                    for note in dev.lastOrders:
                        if cur_type != note.type:
                            cur_type = note.type
                            type_class_id += 1

                        file.w_o_tag(html_defs.T_TR,
                                     html_defs.A_CLASS.format(common.CL_TR_1))

                        # department
                        if first_dep:
                            first_dep = False
                            self.__gen_department(file, dep, str(all_notes))

                        # device name
                        if first_dev:
                            first_dev = False
                            self.__gen_device_name(file, dev.trName, str(len(dev.lastOrders)))

                        # order num
                        self.__gen_order_num(file,
                                             html_defs.A_TITLE.format(
                                                 common.CNT_TXT + str(dev.get_cnt_by_num(note.num))) +
                                             html_defs.A_CLASS.format(common.CL_TD_INC.format(str(type_class_id))),
                                             html_defs.A_HREF.format(
                                                 common.ORDERS_PATH + self.getOrderFileName(name, note.num)),
                                             self.__get_num_by_type(note.type, note.num))


                        # tag date
                        self.__gen_tag_date(file,
                                            note.date,
                                            html_defs.A_TITLE.format(common.TAG_TXT + note.tag)
                                            + html_defs.A_CLASS.format(common.CL_TD_INC.format(str(type_class_id))))

                        # commit hash
                        link_hash = note.pHash
                        if link_hash == -1:
                            link_hash = note.sHash

                        link_to_repo = common.LINK_TO_REPO.format(repo.name,
                                                                  common.GW_SHORTLOG,
                                                                  note.commMsg,
                                                                  str(note.pHash))

                        hash_title = html_defs.A_TITLE.format(self.getTitleForCommit(repo.link,
                                                                                     note.author,note.commDate,
                                                                                     note.commMsg))

                        self.__gen_tag_commit_hash(file,
                                                   html_defs.A_CLASS.format(common.CL_TD_INC.format(str(type_class_id)))
                                                   + hash_title,
                                                   link_to_repo,
                                                   note.sHash + " " + note.commDate)

                        file.write_tag(0, html_defs.T_TR_C)
        out_log(self.__class__.__name__, "finish gen main content")

    def __gen_department(self, file, text, span):
        file.w_tag(html_defs.T_TD,
                   text,
                   html_defs.A_ROWSPAN.format(span))

    def __gen_device_name(self, file, text, span):
        file.w_tag(html_defs.T_TD,
                   text,
                   html_defs.A_ROWSPAN.format(span))

    def __get_num_by_type(self, type, num):
        res = ""
        if common.TYPE_ALL in type:
            res = common.FOR_ALL
        elif common.TYPE_ITEM in type:
            res = common.ITEM_NUM + str(num)
        elif common.TYPE_ORDER in type:
            res = common.ORDER_NUM + str(num)

        return res

    def __gen_order_num(self, file, td_attr, a_link, text):
        self.__gen_linked_td(file, td_attr, a_link, text)

    def __gen_tag_date(self, file, date, attr):
        file.w_tag(html_defs.T_TD,
                   date,
                   attr,
                   True)

    def __gen_tag_commit_hash(self, file, td_attr, a_link, text):
        self.__gen_linked_td(file, td_attr, a_link, text)

    def __gen_linked_td(self, file, td_attr, a_link, text):
        file.w_o_tag(html_defs.T_TD,
                     td_attr,
                     True)
        file.w_tag(html_defs.T_A,
                   text,
                   html_defs.A_HREF.format(a_link))
        file.w_c_tag(html_defs.T_TD)

    def generate_web(self, model):
        time_ch = TimeChecker()
        out_log(self.__class__.__name__, "start gen web")

        time_ch.start
        self.__gen_index(model)
        self.__gen_pages(model)
        time_ch.stop

        out_log(self.__class__.__name__, "finish gen web - " + time_ch.passed_time_str)



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


    def genNoteDate(self, file, date, attr):
        self.genTd(file,
                   str(date),
                   attr)

    def genNoteHash(self, file, hash, attr, title, link):
        self.genTd(file,
                   hash,
                   attr + html_defs.A_TITLE.format(title), link)


    def genOrdersPages(self, dep, device, repoLink, repoName):
        out_log(self.__class__.__name__, "start gen items pages for device: " + device.name)

        for key, val in device.orders.items():
            page = HtmlGen(common.ORDERS_PATH, self.getOrderFileName(device.name, val[0].num))

            self.__gen_page_head(page)
            self.__gen_table_head(page)

            self.gen_order_table_head(page,
                                      [common.HISTORY + device.trName + " - " + self.__get_num_by_type(val[0].type,
                                                                                                       val[0].num),
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
                                 html_defs.A_TITLE.format(common.TAG_TXT + note.tag)
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

            self.__gen_table_foot(page)
            self.genBackLink(page, common.LEVEL_UP + common.LEVEL_UP)
            self.__gen_page_foot_info(page)
            self.__gen_page_foot(page)

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






    def gen_top_table_head(self, gen, attrList):
        gen.write_tag(3, html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.MAIN_T_HD_COL))  # TABLE_HD_COL
        gen.write_tag(4, html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.M_TABLE_COLSPAN))

        for str in attrList:
            gen.write_tag(4, html_defs.T_H3_O)
            self.genFont(gen, str, html_defs.A_COLOR.format(common.WHITE))
            gen.write_tag(4, html_defs.T_H3_C)

        gen.write_tag(0, html_defs.T_TH_C)
        gen.write_tag(0, html_defs.T_TR_C)


    def genTopTableHead(self, gen, text):
        gen.write_tag(0, html_defs.T_TR_O, html_defs.A_BGCOLOR.format(common.MAIN_T_HD_COL)) #TABLE_HD_COL
        gen.write_tag(0, html_defs.T_TH_O, html_defs.A_COLSPAN.format(common.M_TABLE_COLSPAN))
        gen.write_tag(0, html_defs.T_H3_O)
        self.genFont(gen, text, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_H3_C)
        gen.write_tag(0, html_defs.T_H3_O)
        self.genFont(gen, text, html_defs.A_COLOR.format(common.WHITE))
        gen.write_tag(0, html_defs.T_H3_C)
        gen.write_tag(0, html_defs.T_TH_C)
        gen.write_tag(0, html_defs.T_TR_C)








    def gen_device_table_head(self, *args):
        if len(args) < 2:
            return

        self.gen_top_table_head(args[0], args[1:])
        self.__gen_mid_table_head(args[0])
        self.__gen_mid_common_table_body(args[0])
        self.__gen_mid_table_foot(args[0])
        self.__gen_bottom_table_head(args[0])


    def genDeviceTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def gen_order_table_head(self, gen, attrList):
        self.gen_top_table_head(gen, attrList)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def genOrderTableHead(self, gen, text):
        self.genTopTableHead(gen, common.HISTORY + text)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def genBackLink(self, gen, levels):
        gen.write_tag(0, html_defs.T_P_O, html_defs.A_ALIGN.format(common.ALIGN_C))
        gen.write_tag(0, html_defs.T_A_O, html_defs.A_HREF.format(levels + common.MAIN_F_NAME))
        gen.write_tag(0, common.BACK)
        gen.write_tag(0, html_defs.T_A_C)
        gen.write_tag(0, html_defs.T_P_C)


