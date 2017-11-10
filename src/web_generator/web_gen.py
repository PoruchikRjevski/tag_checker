import datetime
import os
from collections import OrderedDict

from web_generator.html_gen import HtmlGen

import common_defs as c_d
import global_vars as g_v
import version as v
from logger import *
from tag_model import *
from web_generator import html_defs as h_d


class WebGenerator:
    def __init__(self):
        if g_v.DEBUG: out_log("init")

        self.__cur_timestamp = None

    def __clear_out_dir(self, dir):
        for item in os.listdir(dir):
            item_path = os.path.join(dir, item)
            if item != c_d.JS_DIR and item != c_d.CSS_DIR:
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        self.__clear_out_dir(item_path)
                except Exception as e:
                    out_err(e)

    def __gen_index(self, model):
        if g_v.DEBUG: out_log("start gen index")
        index = HtmlGen(g_v.OUT_PATH, c_d.INDEX_F_NAME)

        self.__gen_page_head(index, c_d.M_HEAD_TXT, "", h_d.A_CLASS.format(c_d.CL_BACK_CIRLE))

        self.__gen_content_start(index)
        self.__gen_iframe(index)
        self.__gen_script(index, os.path.join(c_d.JS_DIR, c_d.SCRIPTS_F_NAME))
        self.__gen_content_end(index)

        self.__gen_page_foot_info(index)
        self.__gen_page_foot(index)

        index.close()
        if g_v.DEBUG: out_log("finish gen index")

    def __gen_read_metrics_help_page(self):
        if g_v.DEBUG: out_log("start gen read metrics help page")
        help = HtmlGen(g_v.OUT_PATH, c_d.HELP_METR_F_NAME)

        self.__gen_page_head(help, c_d.READ_METR_TXT, "", h_d.A_CLASS.format(c_d.CL_BACK_CIRLE))

        self.__gen_content_start(help)

        self.__gen_rmhp_content(help)

        self.__gen_back_link(help)
        self.__gen_content_end(help)

        self.__gen_page_foot(help)

        help.close()
        if g_v.DEBUG: out_log("finish gen read metrics help page")

    def __gen_rmhp_table_head(self, gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_F),
                    True)
        gen.w_tag(h_d.T_TH,
                  c_d.CLRD_DESIGN_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER + " " + c_d.CL_MID_HEAD)
                  )
        gen.w_tag(h_d.T_TH,
                  c_d.TXT_DESIGN_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_tag(h_d.T_TH,
                  c_d.DESCRIPTION_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_c_tag(h_d.T_TR)

    def __gen_rmhp_content_line(self, gen, color, bg_color, text_design, text_descr):
        gen.w_o_tag(h_d.T_TR,
                     h_d.A_CLASS.format(c_d.CL_TR_1))

        metr_class = h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(0))
                                        + " " + c_d.CL_TEXT_CENTER
                                        + " " + c_d.CL_BORDER)

        gen.w_o_tag(h_d.T_TD,
                    metr_class)
        gen.w_tag(h_d.T_P,
                  2 * h_d.WS,
                  h_d.A_CLASS.format(c_d.CL_TEXT_CENTER
                                     + " " + c_d.CL_NO_WRAP)
                  + (h_d.A_STYLE.format(h_d.A_ST_BAGEL.format(color))))
        gen.w_c_tag(h_d.T_TD)

        gen.w_tag(h_d.T_TD,
                  text_design,
                  metr_class)
        gen.w_tag(h_d.T_TD,
                  text_descr,
                  metr_class)

        gen.w_c_tag(h_d.T_TR)

    def __gen_rmhp_content(self, gen):
        gen.w_o_tag(h_d.T_TABLE,
                    h_d.A_CLASS.format(c_d.CL_HELP_TABLE),
                    True)

        self.__gen_top_main_table_head(gen, c_d.READ_METR_TXT, c_d.H_TABLE_CS)
        self.__gen_rmhp_table_head(gen)

        # gen body table
        self.__gen_rmhp_content_line(gen, c_d.CLR_GREEN, c_d.CLR_GREEN, c_d.CLR_GREEN_TXT,
                                     "Последняя версия по дате коммита(обычно это элемент типа \"Для всех\")")
        self.__gen_rmhp_content_line(gen, c_d.CLR_RED_MIN, c_d.CLR_RED_MIN, c_d.CLR_RED_TXT,
                                     "Версия и дата установки рассматриваемого элемента{:s}, чем у базового.".format(h_d.ARR_DOWN))
        self.__gen_rmhp_content_line(gen, c_d.CLR_YEL, c_d.CLR_YEL, c_d.CLR_YEL_TXT,
                                     "Версия рассматриваемого элемента {:s}, а дата установки {:s}, чем у базового".format(h_d.ARR_DOWN,
                                                                                                                           h_d.ARR_UP))
        self.__gen_rmhp_content_line(gen, c_d.CLR_BLUE, c_d.CLR_BLUE, c_d.CLR_BLUE_TXT,
                                     "Версия и дата установки рассматриваемого элемента {:s}, чем у базового".format(h_d.ARR_UP))

        gen.w_c_tag(h_d.T_TABLE)

    def __gen_pages(self, model):
        if g_v.DEBUG: out_log("start gen main")
        main = HtmlGen(g_v.OUT_PATH, c_d.MAIN_F_NAME)

        self.__gen_page_head(main, c_d.M_HEAD_TXT, "")

        self.__gen_content_start(main)
        self.__gen_table_head(main)
        self.__gen_main_table_head(main)

        self.__gen_main_content(model, main)

        self.__gen_table_foot(main)
        self.__gen_content_end(main)
        self.__gen_page_foot(main)

        main.close()
        if g_v.DEBUG: out_log("finish gen main")

    def __gen_page_head(self, gen, title, level, body_attr=""):
        gen.w_o_tag(h_d.T_HTML, "", True)
        gen.w_o_tag(h_d.T_HEAD, "", True)
        gen.w_o_tag(h_d.T_META, h_d.A_CHARSET.format(c_d.DOC_CODE), True)
        gen.w_o_tag(h_d.T_META,
                    h_d.A_HTTP_EQUIV.format(h_d.A_HE_CACHE_CONTR)
                    + h_d.A_CONTENT.format(h_d.A_C_NO_CACHE + ", "
                                         + h_d.A_C_NO_STORE + ", "
                                         + h_d.A_C_MUST_REVAL),
                    True)
        gen.w_o_tag(h_d.T_META,
                    h_d.A_HTTP_EQUIV.format(h_d.A_HE_PRAGMA)
                    + h_d.A_CONTENT.format(h_d.A_C_NO_CACHE),
                    True)

        gen.w_o_tag(h_d.T_LINK,
                    h_d.A_REL.format(h_d.A_REL_SS)
                    + h_d.A_HREF.format(os.path.join(level, c_d.CSS_DIR, c_d.STYLE_F_NAME)), True)

        gen.w_tag(h_d.T_TITLE, title, "", True)

        self.__gen_script(gen, os.path.join(level, c_d.JS_DIR, c_d.JS_METRICS_F_NAME))

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
                  + h_d.A_NAME.format(c_d.FRAME_ID)
                  + h_d.A_CLASS.format(c_d.CL_IFRAME)
                  + h_d.A_SRC.format(c_d.MAIN_F_NAME))

    def __gen_script(self, gen, script):
        gen.w_tag(h_d.T_SCRIPT,
                  "",
                  h_d.A_TYPE.format(h_d.A_T_JS)
                  + h_d.A_SRC.format(script))

    def __gen_table_head(self, gen):
        gen.w_o_tag(h_d.T_TABLE,
                    h_d.A_CLASS.format(c_d.CL_MAIN_TABLE),
                    True)

    def __gen_table_foot(self, gen):
        gen.w_c_tag(h_d.T_TABLE)

    def __gen_page_foot_info(self, gen):
        gen.w_o_tag(h_d.T_DIV,
                    h_d.A_CLASS.format(c_d.CL_FOOTER))

        # todo add info about flags
        flags_txt = "Флаги: {:s}".format(" -{:s}".format(str(c_d.F_MULT_TXT)) if g_v.MULTITH else ""
                                  + " -{:s}".format(str(c_d.F_LOG_TXT)) if g_v.LOGGING else ""
                                  + " -{:s}".format(str(c_d.F_VERBOSE_TXT)) if g_v.VERBOSE else ""
                                                                                                + " -{:s}".format(str(c_d.F_SUDO_TXT)) if g_v.SUDOER else ""
                                  + " -{:s}".format(str(c_d.F_DEBUG_TXT)) if g_v.DEBUG else ""
                                  + " -{:s}".format(str(c_d.F_TIMINGS_TXT)) if g_v.TIMEOUTS else "")

        gen.w_tag(h_d.T_P,
                  c_d.LAST_UPD_TXT + self.__cur_timestamp,
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO)
                  + h_d.A_TITLE.format(c_d.REPOS_NUM_TXT.format(str(g_v.REPOS_NUM)) + "\n"
                                       + c_d.TAGS_NUM_TXT.format(str(g_v.TAGS_NUM)) + "\n"
                                       + c_d.PROC_TAGS_NUM_TXT.format(str(g_v.PROC_TAGS_NUM)) + "\n"
                                       + c_d.SCAN_TIME_TXT.format(g_v.SCAN_TIME) + "\n"
                                       + flags_txt))

        gen.w_o_tag(h_d.T_P,
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))
        gen.w_txt(c_d.VER_TXT.format(v.V_MAJ,
                                     v.V_MIN,
                                     str(int(v.V_BUILD) - int(v.LAST)),
                                     v.V_BUILD,
                                     "{:s}:".format(v.V_STAT)))
        gen.w_tag(h_d.T_A,
                  "{:s}".format(v.HASH),
                  h_d.A_HREF.format(c_d.LINK_TO_SRC_REPO.format(c_d.GW_SHORTLOG,
                                                                v.HASH,
                                                                v.HASH))
                  + h_d.A_TITLE.format(c_d.LAST_AUTH_TXT.format(v.COMMITER))
                  + h_d.A_TARGET.format(c_d.FRAME_ID))\

        gen.w_txt(" {:s} | {:s} ".format(h_d.WS,
                                         h_d.WS))
        gen.w_tag(h_d.T_A,
                  c_d.READ_METR_TXT,
                  h_d.A_HREF.format(c_d.HELP_METR_F_NAME)
                  + h_d.A_TARGET.format(c_d.FRAME_ID))

        gen.w_c_tag(h_d.T_P)

        gen.w_tag(h_d.T_P,
                  c_d.CR_TXT,
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO))

        gen.w_c_tag(h_d.T_DIV)

    def __gen_main_table_head(self, gen):
        self.__gen_top_main_table_head(gen, c_d.M_HEAD_TXT, c_d.M_TABLE_COLSPAN)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_main_table_body(gen)

    def __gen_top_main_table_head(self, gen, text, columns):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_H),
                    True)
        gen.w_o_tag(h_d.T_TH,
                    h_d.A_COLSPAN.format(columns),
                    True)

        gen.w_tag(h_d.T_H.format(""),
                  text,
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
                  c_d.ITEM_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))

    def __gen_mid_table_foot(self, gen):
        gen.w_tag(h_d.T_TH,
                  c_d.LAST_SET_TXT,
                  h_d.A_COLSPAN.format(c_d.DEV_MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))
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
        gen.w_tag(h_d.T_TH,
                  c_d.METRICS_TXT,
                  h_d.A_ROWSPAN.format(c_d.BTM_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_c_tag(h_d.T_TR)

    def __is_need_update_device_page(self, model, dev_name, dep_name):
        dep = model.departments[dep_name]
        dev_item = None

        for item in dep.items:
            if item.dev_name == dev_name:
                dev_item = item

                break

        if not dev_item is None:
            repo = dep.repos[dev_item.repo_i]

            if UPDATE_FLAG in repo.keys():
                flag = repo[UPDATE_FLAG]

                if not flag is None:
                    return flag

        return False

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
                                       h_d.A_ROWSPAN.format(c_d.BTM_ROWS) + h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(0))
                                                                                               + " " + c_d.CL_BORDER),
                                       [dev_link_attrs])

                file.w_c_tag(h_d.T_TR)

                if self.__is_need_update_device_page(model, dev_name, dep_name):
                    self.__gen_device_page(model, dep_name, dev_name)

        if g_v.DEBUG: out_log("finish gen main content")

    def __gen_department(self, file, text, span):
        file.w_tag(h_d.T_TD,
                   text,
                   h_d.A_ROWSPAN.format(span) + h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(0))
                                                                   + " " + c_d.CL_BORDER))

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

    def __gen_tag_date(self, file, date, attr, date_cl):
        file.w_o_tag(h_d.T_TD, attr)
        file.w_o_tag(h_d.T_P, date_cl)
        file.w_txt(date)
        file.w_c_tag(h_d.T_P)
        file.w_c_tag(h_d.T_TD)

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

        dev_str = "{:s} \"{:s}\" [{:s}]".format(c_d.HISTORY_TXT,
                                                   model.get_tr_dev(dev_name),
                                                   self.__cur_timestamp)
        dep_str = "{:s} {:s}".format(c_d.DEPART_TXT,
                                     str(dep_name))

        dev_tooltip = self.__gen_device_head_tooltip()

        self.__gen_page_head(page, dev_str, c_d.LEVEL_UP)
        self.__gen_content_start(page)
        self.__gen_table_head(page)

        self.__gen_device_table_head(page,
                                     [dev_str, dep_str],
                                     dev_tooltip)

        self.__gen_device_content(page, model, dep_name, dev_name)

        self.__gen_table_foot(page)
        self.__gen_back_link(page)
        self.__gen_content_end(page)

        self.__gen_page_foot(page)

        page.close()

        if g_v.DEBUG: out_log("finish gen pages for device: " + dev_name)

    def __gen_history_page(self, model, dep, dev_name, item_num, type, items):
        if g_v.DEBUG: out_log("start gen item page: " + str(item_num))

        item_file_name = self.__get_item_file_name(dev_name, item_num)
        item_dir_name = self.__get_item_dir_name(dev_name, item_num)

        dev_str = "{:s} \"{:s}\" - \"{:s}\" [{:s}]".format(c_d.HISTORY_TXT,
                                                              model.get_tr_dev(dev_name),
                                                              self.__get_num_by_type(type, item_num),
                                                              self.__cur_timestamp)
        dep_str = "{:s} {:s}".format(c_d.DEPART_TXT,
                                     str(dep.name))

        page = HtmlGen(os.path.join(c_d.ORDERS_PATH, item_dir_name), item_file_name)

        self.__gen_page_head(page, dev_str, c_d.LEVEL_UP * 3)
        self.__gen_content_start(page)
        self.__gen_table_head(page)

        self.__gen_items_table_head(page,
                                    [dev_str, dep_str])

        self.__gen_items_content(page, dep, items)

        self.__gen_table_foot(page)
        self.__gen_back_link(page)
        self.__gen_content_end(page)
        self.__gen_page_foot(page)

        page.close()

        if g_v.DEBUG: out_log("finish gen item page: " + str(item_num))

    def __gen_items_content(self, page, dep, items):
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
            soft_type_class = h_d.A_CLASS.format(type_class_id
                                                 + " " + c_d.CL_TEXT_CENTER
                                                 + " " + c_d.CL_BORDER)
            repo_obj = dep.repos[item.repo_i][REPO_OBJECT]
            self.__gen_item_soft_type(page,
                                      repo_obj.soft_type,
                                      soft_type_class)

            # tag date and commit hash
            self.__gen_common_columns(page,
                                      repo_obj,
                                      dep.commits[item.cm_i],
                                      item,
                                      type_class_id)

            page.w_c_tag(h_d.T_TR)

    def __gen_device_content(self, file, model, dep_name, dev_name):
        dep = model.departments[dep_name]
        dev_items = [item for item in dep.items if item.dev_name == dev_name]

        type_class_id = 0
        for type in c_d.TYPES_L:
            typed_items = [item for item in dev_items if item.item_type == type]

            unic_nums = sorted([key for key in dict.fromkeys([item.item_num for item in typed_items]).keys()],
                               reverse=False)

            for num in unic_nums:
                first_s_t = True
                nummed_items = [item for item in typed_items if item.item_num == num]

                soft_type_by_num = []
                for n_item in nummed_items:
                    s_type = dep.repos[n_item.repo_i][REPO_OBJECT].soft_type
                    if s_type not in soft_type_by_num:
                        soft_type_by_num.append(s_type)

                for soft_t in dep.soft_types:
                    s_typed_items = [item for item in nummed_items if dep.repos[item.repo_i][REPO_OBJECT].soft_type == soft_t]

                    if not s_typed_items:
                        continue

                    ld_item = max(s_typed_items, key=lambda item: item.tag_date)

                    type_class_id_str = c_d.CL_TD_INC.format(str(type_class_id))

                    file.w_o_tag(h_d.T_TR,
                                 h_d.A_CLASS.format(str(type_class_id)) +
                                 h_d.A_ON_MOUSE_OVER.format(c_d.CALC_METRICS_FUNC) +
                                 h_d.A_ON_MOUSE_OUT.format(c_d.CALC_DEF_METR_FUNC))

                    # order num
                    if first_s_t:
                        first_s_t = False
                        order_link_attrs = (self.__get_num_by_type(ld_item.item_type, ld_item.item_num),
                                            os.path.join(c_d.ORDERS_DIR,
                                                         self.__get_item_dir_name(dev_name, ld_item.item_num),
                                                         self.__get_item_file_name(dev_name, ld_item.item_num)),
                                            h_d.A_TITLE.format(c_d.CNT_TXT + str(len(nummed_items))))

                        self.__gen_order_num(file,
                                             h_d.A_CLASS.format(type_class_id_str
                                                                + " " + c_d.CL_TD_NUM
                                                                + " " + c_d.CL_BORDER)
                                             + h_d.A_ROWSPAN.format(str(len(soft_type_by_num))),
                                             [order_link_attrs])

                    # order soft type
                    soft_type_class = h_d.A_CLASS.format(type_class_id_str
                                                         + " " + c_d.CL_TEXT_CENTER
                                                         + " " + c_d.CL_BORDER)
                    self.__gen_item_soft_type(file,
                                              soft_t,
                                              soft_type_class)

                    # tag date and commit hash
                    repo = dep.repos[ld_item.repo_i][REPO_OBJECT]
                    commit = dep.commits[ld_item.cm_i]
                    self.__gen_common_columns(file,
                                              repo,
                                              commit,
                                              ld_item,
                                              type_class_id_str)
                    file.w_c_tag(h_d.T_TR)

                # generate page for item
                self.__gen_history_page(model,
                                        dep,
                                        dev_name,
                                        num,
                                        type,
                                        nummed_items)

            type_class_id += 1

    @staticmethod
    def form_dist_link(commit, repo):
        link = g_v.DIST_LINK_PATTERN

        version_id = "{:s}.{:s}".format(commit.date_full, commit.hash)

        link = link.replace("${dist_prefix}", g_v.DIST_LINK_PREFIX)
        link = link.replace("${sw_module_group_id}", repo.sw_archive_module_group_id)
        link = link.replace("${sw_module_id}", repo.sw_archive_module_id)
        link = link.replace("${sw_module_version_id}", version_id)

        return link

    def __gen_common_columns(self, file, repo, commit, item, type_class_id):
        column_class = h_d.A_CLASS.format(type_class_id
                                          + " " + c_d.CL_TEXT_LEFT
                                          + " " + c_d.CL_BORDER)
        # tag date
        self.__gen_tag_date(file,
                            item.tag_date,
                            column_class,
                            h_d.A_TITLE.format(c_d.TAG_TXT + item.tag)
                            + h_d.A_CLASS.format(c_d.CL_TEXT_LEFT
                                                 + " " + c_d.CL_NO_WRAP))

        # commit hash
        link_hash = commit.p_hash
        if link_hash == -1:
            link_hash = commit.hash

        # list contains tuples (text, link, attr)
        links_list = []

        repo_link_c = (commit.hash + " " + commit.date,
                       c_d.LINK_TO_REPO.format(repo.name, c_d.GW_SHORTLOG,
                                               commit.hash, str(commit.p_hash)),
                       h_d.A_TITLE.format(self.__get_title_for_commit(repo.link, commit.auth,
                                                                      commit.date, commit.msg)))

        links_list.append(repo_link_c)

        ver_class = h_d.A_CLASS.format(type_class_id
                                       + " " + c_d.CL_TD_VER
                                       + " " + c_d.CL_BORDER)

        if item.item_type is c_d.TYPE_ALL:
            ftp_link_c = (c_d.REDIST_TXT,
                          WebGenerator.form_dist_link(commit, repo),
                          h_d.A_TITLE.format(c_d.LINK_FTP_TXT)
                          + h_d.A_TARGET.format(h_d.A_TARGET_BLANK))
            links_list.append(ftp_link_c)

        self.__gen_tag_commit_version(file,
                                      ver_class,
                                      links_list)

        metr_class = h_d.A_CLASS.format(type_class_id
                                        + " " + c_d.CL_TEXT_RIGHT
                                        + " " + c_d.CL_BORDER)
        self.__gen_metrics_column(file, metr_class, item.metric)

    def __gen_metrics_column(self, gen, cl, metric):
        color = 0x00
        p_title = None
        days_text = ""
        mark_text = "-"

        # gen color
        if metric.last:
            color = c_d.CLR_GREEN
            p_title = c_d.CLR_GREEN_TXT
            mark_text = h_d.A_TEXT_CHECK_MARK
        elif metric.forced:
            color = c_d.CLR_YEL
            p_title = c_d.CLR_YEL_TXT
        elif metric.exp:
            color = c_d.CLR_BLUE_MAX - (metric.color_intensity * c_d.CLR_BLUE_STEP)
            p_title = c_d.CLR_BLUE_TXT
            mark_text = "+"
        elif metric.old:
            color = c_d.CLR_RED_MAX - (metric.color_intensity * c_d.CLR_RED_STEP)
            p_title = c_d.CLR_RED_TXT

        colored_thing = h_d.A_ST_BAGEL.format(color)
        # colored_thing = h_d.A_ST_COLORED.format(color)

        # gen text
        if metric.old or metric.forced:
            days_text = "{0:4d} д.".format((-metric.diff_d.days) if metric.diff_d.days > 0 else metric.diff_d.days)
        elif metric.exp:
            days_text = "{0:4d} д.".format(+metric.diff_d.days)
        elif metric.last:
            days_text = "0 д."

        # gen tags
        gen.w_o_tag(h_d.T_TD, cl)

        gen.w_tag(h_d.T_P,
                  days_text,
                  h_d.A_CLASS.format(c_d.CL_TEXT_LEFT
                                     + " " + c_d.CL_NO_WRAP)
                  + h_d.A_TITLE.format("{0:4d} пр.".format(metric.jumps)))

        gen.w_tag(h_d.T_P,
                  # mark_text,
                  2 * h_d.WS,
                  h_d.A_CLASS.format(c_d.CL_TEXT_RIGHT
                                     + " " + c_d.CL_NO_WRAP)
                  + h_d.A_STYLE.format(colored_thing)
                  + (h_d.A_TITLE.format(p_title) if not p_title is None else ""))

        gen.w_c_tag(h_d.T_TD)

    def __change_class_type(self, c_type):
        if c_type == c_d.CL_TD_1:
            c_type = c_d.CL_TD_2
        elif c_type == c_d.CL_TD_2:
            c_type = c_d.CL_TD_1

        return c_type

    def __gen_back_link(self, gen):
        gen.w_o_tag(h_d.T_P,
                    h_d.A_CLASS.format(c_d.CL_FOOT_BACK))
        gen.w_tag(h_d.T_A,
                  c_d.BACK_TXT,
                  h_d.BLK_ONCLICK_BACK)
        gen.w_c_tag(h_d.T_P)

    def __gen_device_head_tooltip(self):
        tooltip = ""

        return tooltip

    def __gen_device_table_head(self, gen, text_list, tooltip):
        self.__gen_top_dev_order_table_head(gen, text_list, tooltip, c_d.D_TABLE_COLSPAN)
        self.__gen_mid_table_head(gen)
        self.__gen_mid_table_mid(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_items_table_head(self, gen, text_list):
        self.__gen_top_dev_order_table_head(gen, text_list, "", c_d.M_TABLE_CS_ITEM)
        self.__gen_mid_table_head(gen)
        # self.__gen_mid_table_mid(gen)
        self.__gen_mid_common_table_body(gen)
        self.__gen_mid_table_foot(gen)
        self.__gen_bottom_table_head(gen)

    def __gen_top_dev_order_table_head(self, gen, text_list, title, span):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_H)
                    + h_d.A_TITLE.format(title),
                    True)
        gen.w_o_tag(h_d.T_TH,
                    h_d.A_COLSPAN.format(span),
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

    def __get_item_file_name(self, name, num):
        return "{:s}_{:s}{:s}".format(name, str(num), c_d.HTML_EXT)

    def __get_item_dir_name(self, name, num):
        return "{:s}_{:s}/".format(name, str(num))

    def __get_device_file_name(self, name):
        return "{:s}{:s}".format(name, c_d.HTML_EXT)

    def __get_title_for_commit(self, repo, author, commDate, commMsg):
        return c_d.REPO_TXT + repo + "\n" \
               + c_d.AUTHOR_TXT + author + "\n" \
               + c_d.COMM_DATE_TXT + commDate + "\n" \
               + c_d.COMM_MSG_SH_TXT.format(commMsg)

    def __set_current_timestamp(self):
        self.__cur_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def generate_web(self, model, partly_update):
        if g_v.DEBUG: out_log("start gen web")

        self.__set_current_timestamp()

        if not partly_update:
            self.__clear_out_dir(g_v.OUT_PATH)

            self.__gen_read_metrics_help_page()

        self.__gen_index(model)
        self.__gen_pages(model)

        if g_v.DEBUG: out_log("finish gen web")

