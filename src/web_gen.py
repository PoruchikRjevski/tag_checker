import datetime
import os

import common_defs as c_d
import global_vars as g_v
import html_defs as h_d
import version as v

from html_gen import HtmlGen
from tag_model import *
from logger import out_log, out_err
from time_checker import *


class WebGenerator:
    def __init__(self):
        if g_v.DEBUG: out_log("init")

    def __gen_index(self, model):
        if g_v.DEBUG: out_log("start gen index")
        index = HtmlGen(g_v.OUT_PATH, c_d.INDEX_F_NAME)

        self.__gen_page_head(index, "", h_d.A_CLASS.format(c_d.CL_BACK_CIRLE))

        self.__gen_content_start(index)
        self.__gen_iframe(index)
        self.__gen_script(index)
        self.__gen_content_end(index)

        self.__gen_page_foot_info(index)
        self.__gen_page_foot(index)

        index.close()
        if g_v.DEBUG: out_log("finish gen index")

    def __gen_pages(self, model):
        if g_v.DEBUG: out_log("start gen main")
        main = HtmlGen(g_v.OUT_PATH, c_d.MAIN_F_NAME)

        self.__gen_page_head(main, "")

        self.__gen_content_start(main)
        self.__gen_table_head(main)
        self.__gen_main_table_head(main)

        self.__gen_main_content(model, main)

        self.__gen_table_foot(main)
        self.__gen_content_end(main)
        self.__gen_page_foot(main)

        main.close()
        if g_v.DEBUG: out_log("finish gen main")

    def __gen_page_head(self, gen, level, body_attr=""):
        gen.w_o_tag(h_d.T_HTML, "", True)
        gen.w_o_tag(h_d.T_HEAD, "", True)
        gen.w_o_tag(h_d.T_META, h_d.A_CHARSET.format(c_d.DOC_CODE), True)
        gen.w_o_tag(h_d.T_LINK,
                    h_d.A_REL.format(h_d.A_REL_SS)
                    + h_d.A_HREF.format(level + c_d.STYLE_F_NAME), True)
        gen.w_c_tag(h_d.T_HEAD)
        gen.w_o_tag(h_d.T_BODY, body_attr, True)
        gen.w_o_tag(h_d.T_DIV,
                    h_d.A_CLASS.format(c_d.CL_WRAPPER))

    def __gen_page_foot(self, gen):
        gen.w_c_tag(h_d.T_DIV)
        gen.w_c_tag(h_d.T_BODY)
        gen.w_c_tag(h_d.T_HTML)

    def __gen_content_start(self, gen):
        gen.w_o_tag(h_d.T_DIV,
                    h_d.A_CLASS.format(c_d.CL_CONTENT))

    def __gen_content_end(self, gen):
        gen.w_c_tag(h_d.T_DIV)

    def __gen_iframe(self, gen):
        gen.w_tag(h_d.T_IFRAME,
                  c_d.FRAME_NOT,
                  h_d.A_ID.format(c_d.FRAME_ID)
                  + h_d.A_CLASS.format(c_d.CL_IFRAME)
                  + h_d.A_SRC.format(c_d.MAIN_F_NAME))

    def __gen_script(self, gen):
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
        gen.w_o_tag(h_d.T_DIV,
                    h_d.A_CLASS.format(c_d.CL_FOOTER))

        gen.w_tag(h_d.T_P,
                  c_d.LAST_UPD_TXT + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))
        gen.w_tag(h_d.T_P,
                  c_d.CR_TXT,
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))
        gen.w_tag(h_d.T_P,
                  c_d.VER_TXT.format(v.V_MAJ, v.V_MIN, str(int(v.V_BUILD) - int(v.LAST)), v.V_BUILD, v.V_STAT),
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))

        gen.w_c_tag(h_d.T_DIV)

    def __gen_main_table_head(self, gen):
        self.__gen_top_main_table_head(gen)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_main_table_body(gen)

    def __gen_top_main_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_H),
                    True)
        gen.w_o_tag(h_d.T_TH,
                    h_d.A_COLSPAN.format(c_d.M_TABLE_COLSPAN) + h_d.A_CLASS.format(c_d.CL_BORDER),
                    True)

        gen.w_tag(h_d.T_H.format(""),
                  c_d.M_HEAD_TXT,
                  h_d.A_CLASS.format(c_d.CL_MAIN_HEAD))

        gen.w_c_tag(h_d.T_TH)
        gen.w_c_tag(h_d.T_TR)

    def __gen_mid_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_F),
                    True)

    def __gen_mid_main_table_body(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.DEP_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER + " " + c_d.CL_MID_HEAD)
                  )
        gen.w_tag(h_d.T_TH,
                  c_d.DEV_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER))

    def __gen_mid_common_table_body(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.SOFT_TYPE_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))

    def __gen_mid_table_mid(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.SOFT_TYPE_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))

    def __gen_mid_table_foot(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.LAST_SET_TXT,
                  h_d.A_COLSPAN.format(c_d.MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_c_tag(h_d.T_TR)

    def __gen_bottom_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_F),
                    True)
        gen.w_tag(h_d.T_TH,
                  c_d.DATE_TXT,
                  h_d.A_ROWSPAN.format(c_d.BTM_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_tag(h_d.T_TH,
                  c_d.HASH_TXT,
                  h_d.A_ROWSPAN.format(c_d.BTM_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_c_tag(h_d.T_TR)

    def __gen_main_content(self, model, file):
        if g_v.DEBUG: out_log("start gen main content")

        for dep_name, dep_obj in model.departments.items():
            first_dep = True
            for dev_name in dep_obj.devices:
                file.w_o_tag(h_d.T_TR,
                             h_d.A_CLASS.format(c_d.CL_TR_1))
                # department
                if first_dep:
                    first_dep = False
                    self.__gen_department(file, dep_name, str(len(dep_obj.devices)))

                # device name
                dev_link_attrs = (model.get_tr_dev(dev_name),
                                  c_d.DEVICE_PATH + self.__get_device_file_name(dev_name),
                                  h_d.A_TITLE.format(c_d.TO_DEV_TXT))
                self.__gen_device_name(file,
                                       h_d.A_ROWSPAN.format(c_d.BTM_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER),
                                       [dev_link_attrs])

                file.w_c_tag(h_d.T_TR)

                # gen device page
                self.__gen_device_page(model, dep_name, dev_name)

        if g_v.DEBUG: out_log("finish gen main content")

    def __gen_department(self, file, text, span):
        file.w_tag(h_d.T_TD,
                   text,
                   h_d.A_ROWSPAN.format(span) + h_d.A_CLASS.format(c_d.CL_BORDER))

    def __gen_device_name(self, file, td_attr, link_attrs):
        self.__gen_linked_td(file, td_attr, link_attrs)

    def __get_num_by_type(self, type, num):
        res = ""

        if c_d.TYPE_ALL in type:
            res = c_d.T_FOR_ALL_TXT
        elif c_d.TYPE_ITEM in type:
            res = c_d.T_ITEM_TXT + str(num)
        elif c_d.TYPE_ORDER in type:
            res = c_d.T_ORDER_TXT + str(num)

        return res

    def __gen_order_num(self, file, td_attr, link_attrs):
        self.__gen_linked_td(file, td_attr, link_attrs)

    def __gen_item_soft_type(self, file, type, attr):
        file.w_tag(h_d.T_TD,
                   type,
                   attr,
                   True)

    def __gen_tag_date(self, file, date, attr):
        file.w_tag(h_d.T_TD,
                   date,
                   attr,
                   True)

    def __gen_tag_commit_version(self, file, td_attr, link_attrs):
        self.__gen_linked_td(file, td_attr, link_attrs)

    def __gen_linked_td(self, file, td_attr, link_attrs):
        file.w_o_tag(h_d.T_TD,
                     td_attr,
                     True)

        file.w_o_tag(h_d.T_P)

        for text, link, title in link_attrs:
            if link and title:
                file.w_tag(h_d.T_A,
                           text,
                           h_d.A_HREF.format(link) + title)
            else:
                file.w_txt(text)

        file.w_c_tag(h_d.T_P)

        file.w_c_tag(h_d.T_TD)

    def __gen_device_page(self, model, dep_name, dev_name):
        if g_v.DEBUG: out_log("start gen pages for device: " + dev_name)
        page = HtmlGen(c_d.DEVICE_PATH, self.__get_device_file_name(dev_name))

        self.__gen_page_head(page, c_d.LEVEL_UP)
        self.__gen_content_start(page)
        self.__gen_table_head(page)

        self.__gen_device_table_head(page,
                                     [c_d.HISTORY_TXT + " \"" + model.get_tr_dev(dev_name) + "\"",
                                      c_d.DEPART_TXT + str(dep_name)])

        self.__gen_device_content(page, model, dep_name, dev_name)

        self.__gen_table_foot(page)
        self.__gen_back_link(page,
                             os.path.join(c_d.LEVEL_UP,
                                          c_d.MAIN_F_NAME))
        self.__gen_content_end(page)

        self.__gen_page_foot(page)

        page.close()

        if g_v.DEBUG: out_log("finish gen pages for device: " + dev_name)

    def __gen_items_page(self, model, dep_name, dev_name, repos, item_num, type, items):
        if g_v.DEBUG: out_log("start gen item page: " + str(item_num))

        page = HtmlGen(c_d.ORDERS_PATH, self.__get_order_file_name(dev_name, item_num))

        self.__gen_page_head(page, c_d.LEVEL_UP * 2)
        self.__gen_content_start(page)
        self.__gen_table_head(page)

        self.__gen_items_table_head(page,
                                    [c_d.HISTORY_TXT + " \"" + model.get_tr_dev(dev_name) + "\"" + " - "
                                     + " \"" + self.__get_num_by_type(type, item_num) + "\"",
                                     c_d.DEPART_TXT + str(dep_name)])

        self.__gen_items_content(page, repos, items)

        self.__gen_table_foot(page)
        self.__gen_back_link(page,
                             os.path.join(c_d.LEVEL_UP,
                                          self.__get_device_file_name(dev_name)))
        self.__gen_content_end(page)
        self.__gen_page_foot(page)

        page.close()

        if g_v.DEBUG: out_log("finish gen item page: " + str(item_num))

    def __gen_items_content(self, page, repos, items):
        type_class_id = c_d.CL_TD_1

        first = True
        date = ""

        items.sort(key=lambda item: item.tag_date, reverse=True)

        for item in items:
            if first:
                first = False
                date = item.tag_date
            else:
                if date not in item.tag_date:
                    date = item.tag_date
                    type_class_id = self.__change_class_type(type_class_id)

            page.w_o_tag(h_d.T_TR,
                         h_d.A_CLASS.format(type_class_id))

            # order soft type
            soft_type_class = h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id))
                                                 + " " + c_d.CL_TEXT_CENTER
                                                 + " " + c_d.CL_BORDER)
            self.__gen_item_soft_type(page,
                                      repos[item.repo_i].soft_type,
                                      soft_type_class)

            # tag date and commit hash
            self.__gen_common_columns(page,
                                      repos[item.repo_i],
                                      item,
                                      type_class_id)

            page.w_c_tag(h_d.T_TR)

    def __gen_device_content(self, file, model, dep_name, dev_name):
        dep = model.departments[dep_name]
        dev_items = [item for item in dep.items if item.dev_name == dev_name]

        type_class_id = 0
        for type in c_d.TYPES_L:
            typed_items = [item for item in dev_items if item.item_type == type]

            unic_nums = [key for key in dict.fromkeys([item.item_num for item in typed_items]).keys()]

            for num in unic_nums:
                first_s_t = True
                nummed_items = [item for item in typed_items if item.item_num == num]

                soft_type_by_num = []
                for n_item in nummed_items:
                    s_type = dep.repos[n_item.repo_i].soft_type
                    if s_type not in soft_type_by_num:
                        soft_type_by_num.append(s_type)

                for soft_t in dep.soft_types:
                    s_typed_items = [item for item in nummed_items if dep.repos[item.repo_i].soft_type == soft_t]

                    if not s_typed_items:
                        continue

                    ld_item = max(s_typed_items, key=lambda item: item.tag_date)

                    file.w_o_tag(h_d.T_TR,
                                 h_d.A_CLASS.format(str(type_class_id)))
                    # order num
                    if first_s_t:
                        first_s_t = False
                        order_link_attrs = (self.__get_num_by_type(ld_item.item_type, ld_item.item_num),
                                            os.path.join(c_d.ORDERS_DIR,
                                                         self.__get_order_file_name(dev_name, ld_item.item_num)),
                                            h_d.A_TITLE.format(c_d.CNT_TXT + str(len(nummed_items))))

                        self.__gen_order_num(file,
                                             h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id))
                                                                + " " + c_d.CL_TD_NUM
                                                                + " " + c_d.CL_BORDER)
                                             + h_d.A_ROWSPAN.format(str(len(soft_type_by_num))),
                                             [order_link_attrs])

                    # order soft type
                    soft_type_class = h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id))
                                                         + " " + c_d.CL_TEXT_CENTER
                                                         + " " + c_d.CL_BORDER)
                    self.__gen_item_soft_type(file,
                                              soft_t,
                                              soft_type_class)

                    # tag date and commit hash
                    repo = model.departments[dep_name].repos[ld_item.repo_i]
                    self.__gen_common_columns(file,
                                              repo,
                                              ld_item,
                                              type_class_id)
                    file.w_c_tag(h_d.T_TR)

                # generate page for item
                self.__gen_items_page(model, dep_name, dev_name, model.departments[dep_name].repos, num, type, nummed_items)

            type_class_id += 1

    def __gen_common_columns(self, file, repo, item, type_class_id):
        tag_date_class = h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id))
                                            + " " + c_d.CL_TEXT_CENTER
                                            + " " + c_d.CL_BORDER)
        # tag date
        self.__gen_tag_date(file,
                            item.tag_date,
                            h_d.A_TITLE.format(c_d.TAG_TXT + item.tag) + tag_date_class)

        # commit hash
        link_hash = item.p_hash
        if link_hash == -1:
            link_hash = item.cm_hash

        # list contains tuples (text, link, attr)
        links_list = []

        repo_link_c = (item.cm_hash + " " + item.cm_date,
                       c_d.LINK_TO_REPO.format(repo.name, c_d.GW_SHORTLOG,
                                               item.cm_hash, str(item.p_hash)),
                       h_d.A_TITLE.format(self.__get_title_for_commit(repo.link, item.cm_auth,
                                                                      item.cm_date, item.cm_msg)))

        links_list.append(repo_link_c)

        ver_class = h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(type_class_id))
                                       + " " + c_d.CL_TD_VER
                                       + " " + c_d.CL_BORDER)

        if item.item_type is c_d.TYPE_ALL:
            ftp_link_c = (c_d.REDIST_TXT,
                          c_d.LINK_TO_FTP.format(item.dev_name, item.cm_hash),
                          h_d.A_TITLE.format(c_d.LINK_FTP_TXT)
                          + h_d.A_TARGET.format(h_d.A_TAR_BLANK))
            links_list.append(ftp_link_c)

        self.__gen_tag_commit_version(file,
                                      ver_class,
                                      links_list)

    def __change_class_type(self, c_type):
        if c_type == c_d.CL_TD_1:
            c_type = c_d.CL_TD_2
        elif c_type == c_d.CL_TD_2:
            c_type = c_d.CL_TD_1

        return c_type

    def __gen_back_link(self, gen, path):
        gen.w_o_tag(h_d.T_P,
                    h_d.A_CLASS.format(c_d.CL_FOOT_BACK))
        gen.w_tag(h_d.T_A,
                  c_d.BACK_TXT,
                  h_d.A_HREF.format(path))
        gen.w_c_tag(h_d.T_P)


    def __gen_device_table_head(self, gen, text_list):
        self.__gen_top_dev_order_table_head(gen, text_list, c_d.D_TABLE_COLSPAN)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_mid(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_items_table_head(self, gen, text_list):
        self.__gen_top_dev_order_table_head(gen, text_list, c_d.M_TABLE_CS_ITEM)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_mid(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_dev_order_table_head(self, gen, text_list, span):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_H),
                    True)
        gen.w_o_tag(h_d.T_TH,
                    h_d.A_COLSPAN.format(span) + h_d.A_CLASS.format(c_d.CL_BORDER),
                    True)

        gen.w_o_tag(h_d.T_H.format(""),
                    "",
                    True)
        for str in text_list:
            gen.w_tag(h_d.T_P,
                      str,
                      "")
        gen.w_c_tag(h_d.T_H.format(""))

        gen.w_c_tag(h_d.T_TH)
        gen.w_c_tag(h_d.T_TR)

    def __get_order_file_name(self, name, num):
        return name + "_" + str(num) + c_d.FILE_EXT

    def __get_device_file_name(self, name):
        return name + c_d.FILE_EXT

    def __get_title_for_commit(self, repo, author, commDate, commMsg):
        return c_d.REPO_TXT + repo + "\n" \
               + c_d.AUTHOR_TXT + author + "\n" \
               + c_d.COMM_DATE_TXT + commDate + "\n" \
               + c_d.COMM_MSG_SH_TXT.format(commMsg)

    def generate_web(self, model):
        if g_v.DEBUG: out_log("start gen web")

        self.__gen_index(model)
        self.__gen_pages(model)

        if g_v.DEBUG: out_log("finish gen web")

