import datetime
import os

import common_defs
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
        index = HtmlGen(common_defs.OUT_PATH, common_defs.INDEX_F_NAME)

        self.__gen_page_head(index,)
        self.__gen_iframe(index)
        self.__gen_script(index, common_defs.FRAME_ID)
        self.__gen_page_foot(index)

        index.close()
        out_log(self.__class__.__name__, "finish gen index")

    def __gen_pages(self, model):
        out_log(self.__class__.__name__, "start gen main")
        main = HtmlGen(common_defs.OUT_PATH, common_defs.MAIN_F_NAME)

        self.__gen_page_head(main)
        self.__gen_table_head(main)
        self.__gen_main_table_head(main)

        self.__gen_main_content(model, main)

        self.__gen_table_foot(main)
        self.__gen_page_foot_info(main)
        self.__gen_page_foot(main)

        main.close()
        out_log(self.__class__.__name__, "finish gen main")

    def __gen_page_head(self, gen, level=""):
        gen.w_o_tag(html_defs.T_HTML, "", True)
        gen.w_o_tag(html_defs.T_HEAD, "", True)
        gen.w_o_tag(html_defs.T_META, html_defs.A_CHARSET.format(common_defs.DOC_CODE), True)
        gen.w_o_tag(html_defs.T_LINK,
                    html_defs.A_REL.format(html_defs.A_REL_SS)
                    + html_defs.A_HREF.format(level + common_defs.STYLE_F_NAME), True)
        gen.w_c_tag(html_defs.T_HEAD)
        gen.w_o_tag(html_defs.T_BODY, "", True)

    def __gen_page_foot(self, gen):
        gen.w_c_tag(html_defs.T_BODY)
        gen.w_c_tag(html_defs.T_HTML)

    def __gen_iframe(self, gen):
        gen.w_tag(html_defs.T_IFRAME,
                  common_defs.FRAME_NOT,
                  html_defs.A_ID.format(common_defs.FRAME_ID) +
                  html_defs.A_STYLE.format(html_defs.A_ST_POS.format(common_defs.FRAME_POS) +
                                           html_defs.A_ST_H.format(common_defs.FRAME_H) +
                                           html_defs.A_ST_W.format(common_defs.FRAME_W) +
                                           html_defs.A_ST_BORDER.format(common_defs.FRAME_BORDER)) +
                  html_defs.A_SRC.format(common_defs.MAIN_F_NAME))

    def __gen_script(self, gen, frame_name):
        gen.w_tag(html_defs.T_SCRIPT,
                  "",
                  html_defs.A_TYPE.format(html_defs.A_T_JS) +
                  html_defs.A_SRC.format(common_defs.SCRIPTS_F_NAME))

    def __gen_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TABLE,
                    html_defs.A_CLASS.format(common_defs.CL_MAIN_TABLE),
                    True)

    def __gen_table_foot(self, gen):
        gen.w_c_tag(html_defs.T_TABLE)

    def __gen_page_foot_info(self, gen):
        gen.w_tag(html_defs.T_P,
                  common_defs.LAST_UPD_TXT + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                  html_defs.A_CLASS.format(common_defs.CL_FOOT_INFO))
        gen.w_tag(html_defs.T_P,
                  common_defs.CR_TXT,
                  html_defs.A_CLASS.format(common_defs.CL_FOOT_INFO))

    def __gen_main_table_head(self, gen):
        self.__gen_top_main_table_head(gen)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_main_table_body(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_main_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common_defs.CL_MT_H),
                    True)
        gen.w_o_tag(html_defs.T_TH,
                    html_defs.A_COLSPAN.format(common_defs.M_TABLE_COLSPAN),
                    True)

        gen.w_tag(html_defs.T_H.format(common_defs.M_TABLE_H_NUM),
                  common_defs.M_HEAD_TXT,
                  "")

        gen.w_c_tag(html_defs.T_TH)
        gen.w_c_tag(html_defs.T_TR)

    def __gen_mid_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common_defs.CL_MT_F),
                    True)

    def __gen_mid_main_table_body(self, gen):
        gen.w_tag(html_defs.T_TH,
                  common_defs.DEP_TXT,
                  html_defs.A_ROWSPAN.format(common_defs.MID_ROWS))
        gen.w_tag(html_defs.T_TH,
                  common_defs.DEV_TXT,
                  html_defs.A_ROWSPAN.format(common_defs.MID_ROWS))

    def __gen_mid_common_table_body(self, gen):
        gen.w_tag(html_defs.T_TH,
                  common_defs.ITEM_TXT,
                  html_defs.A_ROWSPAN.format(common_defs.MID_ROWS))

    def __gen_mid_table_foot(self, gen):
        gen.w_tag(html_defs.T_TH,
                  common_defs.LAST_SET_TXT,
                  html_defs.A_COLSPAN.format(common_defs.MID_ROWS))
        gen.w_c_tag(html_defs.T_TR)

    def __gen_bottom_table_head(self, gen):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common_defs.CL_MT_F),
                    True)
        gen.w_tag(html_defs.T_TH,
                  common_defs.DATE_TXT,
                  html_defs.A_ROWSPAN.format(common_defs.BTM_ROWS))
        gen.w_tag(html_defs.T_TH,
                  common_defs.HASH_TXT,
                  html_defs.A_ROWSPAN.format(common_defs.BTM_ROWS))
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

                        file.w_o_tag(html_defs.T_TR,
                                     html_defs.A_CLASS.format(common_defs.CL_TR_1))

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
                                      common_defs.ORDERS_PATH + self.__get_order_file_name(name, note.num),
                                      html_defs.A_TITLE.format(common_defs.CNT_TXT + str(dev.get_cnt_by_num(note.num))))

                        self.__gen_order_num(file,
                                             html_defs.A_CLASS.format(common_defs.CL_TD_INC.format(str(type_class_id))),
                                             [order_link])

                        # tag date and commit hash
                        tag_date_class = html_defs.A_CLASS.format(common_defs.CL_TD_INC.format(str(type_class_id)) +
                                                                      " " + common_defs.CL_TD_VER)
                        self.__gen_common_columns(file,
                                                  note,
                                                  repo.link,
                                                  repo.name,
                                                  tag_date_class)

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
        if common_defs.TYPE_ALL in type:
            res = common_defs.T_FOR_ALL_TXT
        elif common_defs.TYPE_ITEM in type:
            res = common_defs.T_ITEM_TXT + str(num)
        elif common_defs.TYPE_ORDER in type:
            res = common_defs.T_ORDER_TXT + str(num)

        return res

    def __gen_order_num(self, file, td_attr, links_c_list):
        self.__gen_linked_td(file, td_attr, links_c_list)

    def __gen_tag_date(self, file, date, attr):
        file.w_tag(html_defs.T_TD,
                   date,
                   attr,
                   True)

    def __gen_tag_commit_version(self, file, td_attr, links_c_list):
        self.__gen_linked_td(file, td_attr, links_c_list)

    def __gen_linked_td(self, file, td_attr, links_c_list):
        file.w_o_tag(html_defs.T_TD,
                     td_attr,
                     True)

        file.w_o_tag(html_defs.T_P)

        for text, link, title in links_c_list:
            file.w_tag(html_defs.T_A,
                       text,
                       html_defs.A_HREF.format(link) + title)

        file.w_c_tag(html_defs.T_P)

        file.w_c_tag(html_defs.T_TD)

    def __gen_orders_pages(self, dep, device, repo_link, repo_name):
        out_log(self.__class__.__name__, "start gen items pages for device: " + device.name)

        for key, val in device.orders.items():
            page = HtmlGen(common_defs.ORDERS_PATH, self.__get_order_file_name(device.name, val[0].num))

            self.__gen_page_head(page, common_defs.LEVEL_UP * 2)
            self.__gen_table_head(page)

            self.__gen_order_table_head(page,
                                        [common_defs.HISTORY_TXT, device.trName + " - " +
                                         self.__get_num_by_type(val[0].type,
                                                                val[0].num),
                                         common_defs.DEPART_TXT + str(dep)])

            self.__gen_order_content(page, val, repo_link, repo_name)

            self.__gen_table_foot(page)
            self.__gen_back_link(page, common_defs.LEVEL_UP + common_defs.LEVEL_UP)
            self.__gen_page_foot_info(page)
            self.__gen_page_foot(page)

            page.close()

        out_log(self.__class__.__name__, "finish gen items pages for device: " + device.name)

    def __gen_order_content(self, page, notes, repo_link, repo_name):
        type_class_id = common_defs.CL_TD_1
        date = notes[0].date
        for note in notes:
            if date != note.date:
                date = note.date
                type_class_id = self.__change_class_type(type_class_id)

            page.w_o_tag(html_defs.T_TR,
                         html_defs.A_CLASS.format(type_class_id))

            # tag date and commit hash
            tag_date_class = html_defs.A_CLASS.format(type_class_id + " " + common_defs.CL_TD_VER)
            self.__gen_common_columns(page,
                                      note,
                                      repo_link,
                                      repo_name,
                                      tag_date_class)

            page.w_c_tag(html_defs.T_TR)

    def __gen_common_columns(self, file, note, repo_link, repo_name, tag_date_class):
        # tag date
        self.__gen_tag_date(file,
                            note.date,
                            html_defs.A_TITLE.format(common_defs.TAG_TXT + note.tag) + tag_date_class)

        # commit hash
        link_hash = note.pHash
        if link_hash == -1:
            link_hash = note.sHash


        # list contains tuples (text, link, title)
        links_list = []

        repo_link_c = (note.sHash + " " + note.commDate,
                       common_defs.LINK_TO_REPO.format(repo_name,
                                                       common_defs.GW_SHORTLOG,
                                                       note.sHash,
                                                       str(note.pHash)),
                       html_defs.A_TITLE.format(self.__get_title_for_commit(repo_link, note.author,
                                                                            note.commDate, note.commMsg)))

        links_list.append(repo_link_c)

        if note.type is common_defs.TYPE_ALL:
            ftp_link_c = (common_defs.REDIST_TXT,
                          common_defs.LINK_TO_FTP.format(note.name, note.sHash),
                          html_defs.A_TITLE.format(common_defs.LINK_FTP_TXT))
            links_list.append(ftp_link_c)

        self.__gen_tag_commit_version(file,
                                      tag_date_class,
                                      links_list)

    def __change_class_type(self, type):
        if type == common_defs.CL_TD_1:
            type = common_defs.CL_TD_2
        elif type == common_defs.CL_TD_2:
            type = common_defs.CL_TD_1

        return type

    def __gen_back_link(self, gen, levels):
        gen.w_o_tag(html_defs.T_P,
                    html_defs.A_CLASS.format(common_defs.CL_FOOT_BACK))
        gen.w_tag(html_defs.T_A,
                  common_defs.BACK_TXT,
                  html_defs.A_HREF.format(levels + common_defs.MAIN_F_NAME))
        gen.w_c_tag(html_defs.T_P)

    def __gen_order_table_head(self, gen, text_list):
        self.__gen_top_order_table_head(gen, text_list)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_order_table_head(self, gen, text_list):
        gen.w_o_tag(html_defs.T_TR,
                    html_defs.A_CLASS.format(common_defs.CL_MT_H),
                    True)
        gen.w_o_tag(html_defs.T_TH,
                    html_defs.A_COLSPAN.format(common_defs.M_TABLE_COLSPAN),
                    True)

        gen.w_o_tag(html_defs.T_H.format(common_defs.M_TABLE_H_NUM),
                    "",
                    True)
        for str in text_list:
            gen.w_tag(html_defs.T_P,
                      str,
                      "")
        gen.w_c_tag(html_defs.T_H.format(common_defs.M_TABLE_H_NUM))

        gen.w_c_tag(html_defs.T_TH)
        gen.w_c_tag(html_defs.T_TR)

    def __get_order_file_name(self, name, num):
        return name + "_" + str(num) + common_defs.FILE_EXT

    def __get_title_for_commit(self, repo, author, commDate, commMsg):
        return common_defs.REPO_TXT + repo + "\n" \
               + common_defs.AUTHOR_TXT + author + "\n" \
               + common_defs.COMM_DATE_TXT + commDate + "\n" \
               + common_defs.COMM_MSG_SH_TXT.format(commMsg)

    def generate_web(self, model):
        time_ch = TimeChecker()
        out_log(self.__class__.__name__, "start gen web")

        time_ch.start
        self.__gen_index(model)
        self.__gen_pages(model)
        time_ch.stop

        out_log(self.__class__.__name__, "finish gen web - " + time_ch.passed_time_str)

