import datetime
import os

import common_defs as c_d
import global_vars as g_v
import html_defs as h_d

from html_gen import HtmlGen
from tag_model import TagModel, Device, Note, Repo
from logger import out_log, out_err
from time_checker import TimeChecker


class WebGenerator:
    def __init__(self):
        out_log("init")

    def __join_paths(self, first, sec):
        return os.path.join(first, sec)

    def __gen_index(self, model):
        out_log("start gen index")
        index = HtmlGen(g_v.OUT_PATH, c_d.INDEX_F_NAME)

        self.__gen_page_head(index,)
        self.__gen_iframe(index)
        self.__gen_script(index, c_d.FRAME_ID)
        self.__gen_page_foot(index)

        index.close()
        out_log("finish gen index")

    def __gen_pages(self, model):
        out_log("start gen main")
        main = HtmlGen(g_v.OUT_PATH, c_d.MAIN_F_NAME)

        self.__gen_page_head(main)
        self.__gen_table_head(main)
        self.__gen_main_table_head(main)

        self.__gen_main_content(model, main)

        self.__gen_table_foot(main)
        self.__gen_page_foot_info(main)
        self.__gen_page_foot(main)

        main.close()
        out_log("finish gen main")

    def __gen_page_head(self, gen, level=""):
        gen.w_o_tag(h_d.T_HTML, "", True)
        gen.w_o_tag(h_d.T_HEAD, "", True)
        gen.w_o_tag(h_d.T_META, h_d.A_CHARSET.format(c_d.DOC_CODE), True)
        gen.w_o_tag(h_d.T_LINK,
                    h_d.A_REL.format(h_d.A_REL_SS)
                    + h_d.A_HREF.format(level + c_d.STYLE_F_NAME), True)
        gen.w_c_tag(h_d.T_HEAD)
        gen.w_o_tag(h_d.T_BODY, "", True)

    def __gen_page_foot(self, gen):
        gen.w_c_tag(h_d.T_BODY)
        gen.w_c_tag(h_d.T_HTML)

    def __gen_iframe(self, gen):
        gen.w_tag(h_d.T_IFRAME,
                  c_d.FRAME_NOT,
                  h_d.A_ID.format(c_d.FRAME_ID)
                  + h_d.A_STYLE.format(h_d.A_ST_POS.format(c_d.FRAME_POS)
                                     + h_d.A_ST_H.format(c_d.FRAME_H)
                                     + h_d.A_ST_W.format(c_d.FRAME_W)
                                     + h_d.A_ST_BORDER.format(c_d.FRAME_BORDER))
                  + h_d.A_SRC.format(c_d.MAIN_F_NAME))

    def __gen_script(self, gen, frame_name):
        gen.w_tag(h_d.T_SCRIPT,
                  "",
                  h_d.A_TYPE.format(h_d.A_T_JS)
                  + h_d.A_SRC.format(c_d.SCRIPTS_F_NAME))

    def __gen_table_head(self, gen):
        gen.w_o_tag(h_d.T_TABLE,
                    h_d.A_CLASS.format(c_d.CL_MAIN_TABLE),
                    True)

    def __gen_table_foot(self, gen):
        gen.w_c_tag(h_d.T_TABLE)

    def __gen_page_foot_info(self, gen):
        gen.w_tag(h_d.T_P,
                  c_d.LAST_UPD_TXT + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))
        gen.w_tag(h_d.T_P,
                  c_d.CR_TXT,
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))

    def __gen_main_table_head(self, gen):
        self.__gen_top_main_table_head(gen)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_main_table_body(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_main_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_H),
                    True)
        gen.w_o_tag(h_d.T_TH,
                    h_d.A_COLSPAN.format(c_d.M_TABLE_COLSPAN),
                    True)

        gen.w_tag(h_d.T_H.format(c_d.M_TABLE_H_NUM),
                  c_d.M_HEAD_TXT,
                  "")

        gen.w_c_tag(h_d.T_TH)
        gen.w_c_tag(h_d.T_TR)

    def __gen_mid_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_F),
                    True)

    def __gen_mid_main_table_body(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.DEP_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS))
        gen.w_tag(h_d.T_TH,
                  c_d.DEV_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS))

    def __gen_mid_common_table_body(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.ITEM_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS))

    def __gen_mid_table_foot(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.LAST_SET_TXT,
                  h_d.A_COLSPAN.format(c_d.MID_ROWS))
        gen.w_c_tag(h_d.T_TR)

    def __gen_bottom_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_F),
                    True)
        gen.w_tag(h_d.T_TH,
                  c_d.DATE_TXT,
                  h_d.A_ROWSPAN.format(c_d.BTM_ROWS))
        gen.w_tag(h_d.T_TH,
                  c_d.HASH_TXT,
                  h_d.A_ROWSPAN.format(c_d.BTM_ROWS))
        gen.w_c_tag(h_d.T_TR)

    def __gen_main_content(self, model, file):
        out_log("start gen main content")

        deps = model.departments

        for dep, repos in deps.items():
            first_dep = True
            all_notes = 0

            for repo in repos:
                for name, dev in repo.devices.items():
                    all_notes += len(dev.lastOrders)
                    out_log("Notes for dev: " + name + " - " + str(all_notes))

            for repo in repos:
                for name, dev in repo.devices.items():
                    # generate device's own page
                    self.__gen_orders_pages(dep, dev, repo.link, repo.name)

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

                        file.w_o_tag(h_d.T_TR,
                                     h_d.A_CLASS.format(c_d.CL_TR_1))

                        # department
                        if first_dep:
                            first_dep = False
                            self.__gen_department(file, dep, str(all_notes))

                        # device name
                        if first_dev:
                            first_dev = False
                            self.__gen_device_name(file, dev.trName, str(len(dev.lastOrders)))

                        # order num
                        order_link = (self.__get_num_by_type(note.type, note.num),
                                      c_d.ORDERS_PATH + self.__get_order_file_name(name, note.num),
                                      h_d.A_TITLE.format(c_d.CNT_TXT + str(dev.get_cnt_by_num(note.num))))

                        self.__gen_order_num(file,
                                             h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id))
                                                                + " " + c_d.CL_TD_NUM),
                                             [order_link])

                        # tag date and commit hash
                        tag_date_class = h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id)) +
                                                                      " " + c_d.CL_TD_VER)
                        self.__gen_common_columns(file,
                                                  note,
                                                  repo.link,
                                                  repo.name,
                                                  tag_date_class)
                        file.w_c_tag(h_d.T_TR)
        out_log("finish gen main content")

    def __gen_department(self, file, text, span):
        file.w_tag(h_d.T_TD,
                   text,
                   h_d.A_ROWSPAN.format(span))

    def __gen_device_name(self, file, text, span):
        file.w_tag(h_d.T_TD,
                   text,
                   h_d.A_ROWSPAN.format(span))

    def __get_num_by_type(self, type, num):
        res = ""

        if c_d.TYPE_ALL in type:
            res = c_d.T_FOR_ALL_TXT
        elif c_d.TYPE_ITEM in type:
            res = c_d.T_ITEM_TXT + str(num)
        elif c_d.TYPE_ORDER in type:
            res = c_d.T_ORDER_TXT + str(num)

        return res

    def __gen_order_num(self, file, td_attr, links_c_list):
        self.__gen_linked_td(file, td_attr, links_c_list)

    def __gen_tag_date(self, file, date, attr):
        file.w_tag(h_d.T_TD,
                   date,
                   attr,
                   True)

    def __gen_tag_commit_version(self, file, td_attr, links_c_list):
        self.__gen_linked_td(file, td_attr, links_c_list)

    def __gen_linked_td(self, file, td_attr, links_c_list):
        file.w_o_tag(h_d.T_TD,
                     td_attr,
                     True)

        file.w_o_tag(h_d.T_P)

        for text, link, title in links_c_list:
            file.w_tag(h_d.T_A,
                       text,
                       h_d.A_HREF.format(link) + title)

        file.w_c_tag(h_d.T_P)

        file.w_c_tag(h_d.T_TD)

    def __gen_orders_pages(self, dep, device, repo_link, repo_name):
        out_log("start gen items pages for device: " + device.name)

        for key, val in device.orders.items():
            page = HtmlGen(c_d.ORDERS_PATH, self.__get_order_file_name(device.name, val[0].num))

            self.__gen_page_head(page, c_d.LEVEL_UP * 2)
            self.__gen_table_head(page)

            self.__gen_order_table_head(page,
                                        [c_d.HISTORY_TXT, device.trName + " - " +
                                         self.__get_num_by_type(val[0].type,
                                                                val[0].num),
                                         c_d.DEPART_TXT + str(dep)])

            self.__gen_order_content(page, val, repo_link, repo_name)

            self.__gen_table_foot(page)
            self.__gen_back_link(page, c_d.LEVEL_UP * 2)
            self.__gen_page_foot_info(page)
            self.__gen_page_foot(page)

            page.close()

        out_log("finish gen items pages for device: " + device.name)

    def __gen_order_content(self, page, notes, repo_link, repo_name):
        type_class_id = c_d.CL_TD_1
        date = notes[0].date
        for note in notes:
            if date != note.date:
                date = note.date
                type_class_id = self.__change_class_type(type_class_id)

            page.w_o_tag(h_d.T_TR,
                         h_d.A_CLASS.format(type_class_id))

            # tag date and commit hash
            tag_date_class = h_d.A_CLASS.format(type_class_id + " " + c_d.CL_TD_VER)
            self.__gen_common_columns(page,
                                      note,
                                      repo_link,
                                      repo_name,
                                      tag_date_class)

            page.w_c_tag(h_d.T_TR)

    def __gen_common_columns(self, file, note, repo_link, repo_name, tag_date_class):
        # tag date
        self.__gen_tag_date(file,
                            note.date,
                            h_d.A_TITLE.format(c_d.TAG_TXT + note.tag) + tag_date_class)

        # commit hash
        link_hash = note.pHash
        if link_hash == -1:
            link_hash = note.sHash

        # list contains tuples (text, link, attr)
        links_list = []

        repo_link_c = (note.sHash + " " + note.commDate,
                       c_d.LINK_TO_REPO.format(repo_name, c_d.GW_SHORTLOG,
                                               note.sHash, str(note.pHash)),
                       h_d.A_TITLE.format(self.__get_title_for_commit(repo_link, note.author,
                                                                      note.commDate, note.commMsg)))

        links_list.append(repo_link_c)

        if note.type is c_d.TYPE_ALL:
            ftp_link_c = (c_d.REDIST_TXT,
                          c_d.LINK_TO_FTP.format(note.name, note.sHash),
                          h_d.A_TITLE.format(c_d.LINK_FTP_TXT)
                          + h_d.A_TARGET.format(h_d.A_TAR_BLANK))
            links_list.append(ftp_link_c)

        self.__gen_tag_commit_version(file,
                                      tag_date_class,
                                      links_list)

    def __change_class_type(self, c_type):
        if c_type == c_d.CL_TD_1:
            c_type = c_d.CL_TD_2
        elif c_type == c_d.CL_TD_2:
            c_type = c_d.CL_TD_1

        return c_type

    def __gen_back_link(self, gen, levels):
        gen.w_o_tag(h_d.T_P,
                    h_d.A_CLASS.format(c_d.CL_FOOT_BACK))
        gen.w_tag(h_d.T_A,
                  c_d.BACK_TXT,
                  h_d.A_HREF.format(levels + c_d.MAIN_F_NAME))
        gen.w_c_tag(h_d.T_P)

    def __gen_order_table_head(self, gen, text_list):
        self.__gen_top_order_table_head(gen, text_list)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_order_table_head(self, gen, text_list):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_H),
                    True)
        gen.w_o_tag(h_d.T_TH,
                    h_d.A_COLSPAN.format(c_d.M_TABLE_COLSPAN),
                    True)

        gen.w_o_tag(h_d.T_H.format(c_d.M_TABLE_H_NUM),
                    "",
                    True)
        for str in text_list:
            gen.w_tag(h_d.T_P,
                      str,
                      "")
        gen.w_c_tag(h_d.T_H.format(c_d.M_TABLE_H_NUM))

        gen.w_c_tag(h_d.T_TH)
        gen.w_c_tag(h_d.T_TR)

    def __get_order_file_name(self, name, num):
        return name + "_" + str(num) + c_d.FILE_EXT

    def __get_title_for_commit(self, repo, author, commDate, commMsg):
        return c_d.REPO_TXT + repo + "\n" \
               + c_d.AUTHOR_TXT + author + "\n" \
               + c_d.COMM_DATE_TXT + commDate + "\n" \
               + c_d.COMM_MSG_SH_TXT.format(commMsg)

    def generate_web(self, model):
        time_ch = TimeChecker()
        out_log("start gen web")

        time_ch.start
        self.__gen_index(model)
        self.__gen_pages(model)
        time_ch.stop

        out_log("finish gen web - " + time_ch.passed_time_str)

