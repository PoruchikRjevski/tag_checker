import os
import logging
import datetime
from collections import OrderedDict

from config_manager import dir_man
from web_generator.html_gen import HtmlGen

import common_defs as c_d
import global_vars as g_v
import version as v
from tag_model import *
from web_generator import html_defs as h_d
from logger import log_func_name


__all__ = ['WebGenerator']


logger = logging.getLogger("{:s}.HtmlGen".format(c_d.SOLUTION))


class WebGenerator:
    def __init__(self):
        logger.info("init")

        self.__cur_timestamp = None

    @staticmethod
    @log_func_name(logger)
    def __clear_out_dir(dir):
        for item in os.listdir(dir):
            item_path = os.path.join(dir, item)
            if item != c_d.JS_DIR and item != c_d.CSS_DIR:
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        WebGenerator.__clear_out_dir(item_path)
                except Exception as e:
                    logger.error(e)

    @log_func_name(logger)
    def __gen_index(self, model):
        logger.info("start gen index")
        index = HtmlGen(dir_man.g_dir_man.output_dir, c_d.INDEX_F_NAME)

        WebGenerator.__gen_page_head(index, c_d.M_HEAD_TXT, "", h_d.A_CLASS.format(c_d.CL_BACK_CIRLE))

        WebGenerator.__gen_content_start(index)
        WebGenerator.__gen_iframe(index)
        WebGenerator.__gen_script(index, WebGenerator.join_path(c_d.JS_DIR, c_d.SCRIPTS_F_NAME))
        WebGenerator.__gen_content_end(index)

        self.__gen_page_foot_info(index, model)
        WebGenerator.__gen_page_foot(index)

        index.close()
        logger.info("finish gen index")

    @staticmethod
    @log_func_name(logger)
    def __gen_read_metrics_help_page():
        help_p = HtmlGen(dir_man.g_dir_man.output_dir, c_d.HELP_METR_F_NAME)

        WebGenerator.__gen_page_head(help_p, c_d.READ_METR_TXT, "", h_d.A_CLASS.format(c_d.CL_BACK_CIRLE))

        WebGenerator.__gen_content_start(help_p)

        WebGenerator.__gen_rmhp_content(help_p)

        WebGenerator.__gen_back_link(help_p)
        WebGenerator.__gen_content_end(help_p)

        WebGenerator.__gen_page_foot(help_p)

        help_p.close()

    @staticmethod
    def __gen_rmhp_table_head(gen):
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

    @staticmethod
    def __gen_rmhp_content_line(gen, color, text_design, text_descr):
        gen.w_o_tag(h_d.T_TR, h_d.A_CLASS.format(c_d.CL_TR_1), True)

        metr_class = h_d.A_CLASS.format(c_d.CL_BLACK_TEXT
                                        + " " + c_d.CL_TEXT_CENTER)

        gen.w_o_tag(h_d.T_TD, metr_class, True)
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

    @staticmethod
    def __gen_rmhp_content(gen):
        gen.w_o_tag(h_d.T_TABLE,
                    h_d.A_CLASS.format(c_d.CL_HELP_TABLE),
                    True)

        WebGenerator.__gen_top_main_table_head(gen, c_d.READ_METR_TXT, c_d.H_TABLE_CS)
        WebGenerator.__gen_rmhp_table_head(gen)

        # gen body table
        WebGenerator.__gen_rmhp_content_line(gen, c_d.CLR_GREEN, c_d.CLR_GREEN_TXT,
                                     "Последняя версия по дате установки(обычно это элемент типа \"Для всех\")")
        WebGenerator.__gen_rmhp_content_line(gen, c_d.CLR_RED_MIN, c_d.CLR_RED_TXT,
                                     "Версия и дата установки рассматриваемого элемента{:s}, чем у базового.".format(h_d.ARR_DOWN))
        WebGenerator.__gen_rmhp_content_line(gen, c_d.CLR_YEL, c_d.CLR_YEL_TXT,
                                     "Версия рассматриваемого элемента {:s}, а дата установки {:s}, чем у базового".format(h_d.ARR_DOWN,
                                                                                                                           h_d.ARR_UP))
        WebGenerator.__gen_rmhp_content_line(gen, c_d.CLR_BLUE, c_d.CLR_BLUE_TXT,
                                     "Версия и дата установки рассматриваемого элемента {:s}, чем у базового".format(h_d.ARR_UP))

        gen.w_c_tag(h_d.T_TABLE)

    @log_func_name(logger)
    def __gen_pages(self, model):
        main = HtmlGen(dir_man.g_dir_man.output_dir, c_d.MAIN_F_NAME)

        WebGenerator.__gen_page_head(main, c_d.M_HEAD_TXT, "")

        WebGenerator.__gen_content_start(main)
        WebGenerator.__gen_table_head(main)
        WebGenerator.__gen_main_table_head(main)

        self.__gen_main_content(model, main)

        WebGenerator.__gen_table_foot(main)
        WebGenerator.__gen_content_end(main)
        WebGenerator.__gen_page_foot(main)

        main.close()

    @staticmethod
    def join_path(root, *items):
        res = root
        for i in items:
            if res:
                res = res + "/" + i
            else:
                res = i
        return res

    @staticmethod
    def __gen_page_head(gen, title, level, body_attr=""):
        gen.w_o_tag(h_d.T_HTML, "", True)
        gen.w_o_tag(h_d.T_HEAD, "", True)
        gen.w_o_tag(h_d.T_META, h_d.A_CHARSET.format(c_d.DOC_ENCODING), True)
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
                    + h_d.A_HREF.format(WebGenerator.join_path(level, c_d.CSS_DIR, c_d.STYLE_F_NAME)), True)

        gen.w_tag(h_d.T_TITLE, title, "")

        gen.w_c_tag(h_d.T_HEAD)
        gen.w_o_tag(h_d.T_BODY, body_attr, True)
        gen.w_o_tag(h_d.T_DIV,
                    h_d.A_CLASS.format(c_d.CL_WRAPPER))

    @staticmethod
    def __gen_page_foot(gen):
        gen.w_c_tag(h_d.T_DIV)
        gen.w_c_tag(h_d.T_BODY)
        gen.w_c_tag(h_d.T_HTML)

    @staticmethod
    def __gen_content_start(gen):
        gen.w_o_tag(h_d.T_DIV, h_d.A_CLASS.format(c_d.CL_CONTENT), True)

    @staticmethod
    def __gen_content_end(gen):
        gen.w_c_tag(h_d.T_DIV)

    @staticmethod
    def __gen_iframe(gen):
        gen.w_tag(h_d.T_IFRAME,
                  c_d.FRAME_NOT,
                  h_d.A_ID.format(c_d.FRAME_ID)
                  + h_d.A_NAME.format(c_d.FRAME_ID)
                  + h_d.A_CLASS.format(c_d.CL_IFRAME)
                  + h_d.A_SRC.format(c_d.MAIN_F_NAME))

    @staticmethod
    def __gen_script(gen, script):
        gen.w_tag(h_d.T_SCRIPT,
                  "",
                  h_d.A_TYPE.format(h_d.A_T_JS)
                  + h_d.A_SRC.format(script))

    @staticmethod
    def __gen_table_head(gen):
        gen.w_o_tag(h_d.T_TABLE,
                    h_d.A_CLASS.format(c_d.CL_MAIN_TABLE),
                    True)

    @staticmethod
    def __gen_table_foot(gen):
        gen.w_c_tag(h_d.T_TABLE)

    @staticmethod
    def __get_updated_devices_str(model):
        updated_list = []

        for dep_name, dep_obj in model.departments.items():
            updated_list += [model.get_tr_dev(dev_name) for dev_name, updated_flag in dep_obj.devices.items() if updated_flag]

        return ", ".join(updated_list)

    def __gen_page_foot_info(self, gen, model):
        gen.w_o_tag(h_d.T_DIV,
                    h_d.A_CLASS.format(c_d.CL_FOOTER))

        flags_txt = "Флаги: {:s}".format((" -{:s}".format(str(c_d.F_MULT_TXT)) if g_v.MULTITH else "")
                                         + (" -{:s}".format(str(c_d.F_LOG_TXT)) if g_v.LOGGING else "")
                                         + (" -{:s}".format(str(c_d.F_VERBOSE_TXT)) if g_v.VERBOSE else "")
                                         + (" -{:s}".format(str(c_d.F_DEBUG_TXT)) if g_v.DEBUG else "")
                                         + (" -{:s}".format(str(c_d.F_TIMINGS_TXT)) if g_v.TIMEOUTS else ""))

        updated_devices_txt = c_d.UPDATED_DEVS_TXT.format(WebGenerator.__get_updated_devices_str(model))

        gen.w_tag(h_d.T_P,
                  c_d.LAST_UPD_TXT + self.__cur_timestamp,
                  h_d.A_CLASS.format(c_d.CL_FOOT_INFO)
                  + h_d.A_TITLE.format(c_d.REPOS_NUM_TXT.format(str(g_v.REPOS_NUM)) + "\n"
                                       + c_d.TAGS_NUM_TXT.format(str(g_v.TAGS_NUM)) + "\n"
                                       + c_d.PROC_TAGS_NUM_TXT.format(str(g_v.PROC_TAGS_NUM)) + "\n"
                                       + c_d.SCAN_TIME_TXT.format(g_v.SCAN_TIME) + "\n"
                                       + flags_txt + "\n"
                                       + updated_devices_txt))

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

    @staticmethod
    def __gen_main_table_head(gen):
        WebGenerator.__gen_top_main_table_head(gen, c_d.M_HEAD_TXT, c_d.M_TABLE_COLSPAN)
        WebGenerator.__gen_mid_table_head(gen)
        WebGenerator.__gen_mid_main_table_body(gen)

    @staticmethod
    def __gen_top_main_table_head(gen, text, columns):
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

    @staticmethod
    def __gen_mid_table_head(gen):
        gen.w_o_tag(h_d.T_TR,
                    h_d.A_CLASS.format(c_d.CL_MT_F),
                    True)

    @staticmethod
    def __gen_mid_main_table_body(gen):
        gen.w_tag(h_d.T_TH,
                  c_d.DEP_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER + " " + c_d.CL_MID_HEAD))
        gen.w_tag(h_d.T_TH,
                  c_d.DEV_TXT,
                  h_d.A_CLASS.format(c_d.CL_BORDER))

    @staticmethod
    def __gen_mid_common_table_body(gen):
        gen.w_tag(h_d.T_TH,
                  c_d.SOFT_TYPE_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))

    @staticmethod
    def __gen_mid_table_mid(gen):
        gen.w_tag(h_d.T_TH,
                  c_d.ITEM_TXT,
                  h_d.A_ROWSPAN.format(c_d.MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))

    @staticmethod
    def __gen_mid_table_foot(gen):
        gen.w_tag(h_d.T_TH,
                  c_d.LAST_SET_TXT,
                  h_d.A_COLSPAN.format(c_d.DEV_MID_ROWS) + h_d.A_CLASS.format(c_d.CL_BORDER))
        gen.w_c_tag(h_d.T_TR)

    @staticmethod
    def __gen_bottom_table_head(gen):
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

    @staticmethod
    def __is_need_update_device_page(model, dev_name, dep_name):
        dep = model.departments[dep_name]
        dev_item = None

        for item in dep.items:
            if item.device_class == dev_name:
                dev_item = item

                break

        if not dev_item is None:
            repo = dep.repos[dev_item.repo_index]

            if UPDATE_FLAG in repo.keys():
                flag = repo[UPDATE_FLAG]

                if not flag is None:
                    return flag

        return False

    @log_func_name(logger)
    def __gen_main_content(self, model, file):
        sorted_dps = sorted(model.departments)
        for dep_name in sorted_dps:
            dep_obj = model.departments[dep_name]
            first_dep = True
            sorted_devs = sorted(dep_obj.devices)
            for dev_name in sorted_devs:
                dev_updated = dep_obj.devices[dev_name]
                file.w_o_tag(h_d.T_TR,
                                 h_d.A_CLASS.format(c_d.CL_TR_1))
                # department
                if first_dep:
                    first_dep = False
                    WebGenerator.__gen_department(file, dep_name, str(len(dep_obj.devices)))

                # device name
                dev_link_attrs = (model.get_tr_dev(dev_name),
                                  WebGenerator.join_path(c_d.OUTPUT_DEVICE_REL_DIR, WebGenerator.__get_device_file_name(dev_name)),
                                  h_d.A_TITLE.format(c_d.TO_DEV_TXT))
                WebGenerator.__gen_device_name(file,
                                               h_d.A_ROWSPAN.format(c_d.BTM_ROWS)
                                               + h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(0))
                                                                    + " " + c_d.CL_BORDER),
                                               [dev_link_attrs])

                file.w_c_tag(h_d.T_TR)

                if WebGenerator.__is_need_update_device_page(model, dev_name, dep_name):
                    self.__gen_device_page(model, dep_name, dev_name)

    @staticmethod
    def __gen_department(file, text, span):
        file.w_tag(h_d.T_TD,
                   text,
                   h_d.A_ROWSPAN.format(span) + h_d.A_CLASS.format(c_d.CL_TD_INC.format(str(0))
                                                                   + " " + c_d.CL_BORDER
                                                                   + " " + c_d.CL_BLACK_TEXT))

    @staticmethod
    def __gen_device_name(file, td_attr, link_attrs):
        WebGenerator.__gen_linked_td(file, td_attr, link_attrs)

    @staticmethod
    def __get_num_by_type(type, num):
        res = ""

        if c_d.TAG_DEVICE_SELECTOR_TYPE_ALL in type:
            res = c_d.T_FOR_ALL_TXT
        elif c_d.TAG_DEVICE_SELECTOR_TYPE_ITEM in type:
            res = c_d.T_ITEM_TXT + str(num)
        elif c_d.TAG_DEVICE_SELECTOR_TYPE_SERIE in type:
            res = c_d.T_ORDER_TXT + str(num)

        return res

    @staticmethod
    def __gen_order_num(file, td_attr, link_attrs):
        WebGenerator.__gen_linked_td(file, td_attr, link_attrs)

    @staticmethod
    def __gen_item_soft_type(file, type, attr):
        file.w_tag(h_d.T_TD,
                   type,
                   attr,
                   True)

    @staticmethod
    def __gen_tag_date(file, date, attr, date_cl):
        file.w_o_tag(h_d.T_TD, attr)
        file.w_o_tag(h_d.T_P, date_cl)
        file.w_txt(date)
        file.w_c_tag(h_d.T_P)
        file.w_c_tag(h_d.T_TD)

    @staticmethod
    def __gen_tag_commit_version(file, td_attr, link_attrs):
        WebGenerator.__gen_linked_td(file, td_attr, link_attrs)

    @staticmethod
    def __gen_linked_td(file, td_attr, link_attrs):
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
        logger.info("start gen pages for device: {:s}".format(dev_name))
        page = HtmlGen(dir_man.g_dir_man.output_device_dir, WebGenerator.__get_device_file_name(dev_name))

        dev_str = "{:s} \"{:s}\" [{:s}]".format(c_d.HISTORY_TXT,
                                                model.get_tr_dev(dev_name),
                                                self.__cur_timestamp)
        dep_str = "{:s} {:s}".format(c_d.DEPART_TXT,
                                     str(dep_name))

        dev_tooltip = WebGenerator.__gen_device_head_tooltip()

        WebGenerator.__gen_page_head(page, dev_str, c_d.LEVEL_UP)
        WebGenerator.__gen_content_start(page)
        WebGenerator.__gen_table_head(page)

        WebGenerator.__gen_device_table_head(page,
                                             [dev_str, dep_str],
                                             dev_tooltip)

        self.__gen_device_content(page, model, dep_name, dev_name)

        WebGenerator.__gen_table_foot(page)
        WebGenerator.__gen_back_link(page)
        WebGenerator.__gen_content_end(page)

        WebGenerator.__gen_page_foot(page)

        page.close()

        logger.info("finish gen pages for device: {:s}".format(dev_name))

    def __gen_history_page(self, model, dep, dev_name, device_selector_id, type, items):
        logger.info("start gen item page: {:s}".format(str(device_selector_id)))

        item_file_name = WebGenerator.__get_item_file_name(dev_name, device_selector_id)
        item_dir_name = WebGenerator.__get_item_dir_name(dev_name, device_selector_id)

        dev_str = "{:s} \"{:s}\" - \"{:s}\" [{:s}]".format(c_d.HISTORY_TXT,
                                                           model.get_tr_dev(dev_name),
                                                           WebGenerator.__get_num_by_type(type, device_selector_id),
                                                           self.__cur_timestamp)
        dep_str = "{:s} {:s}".format(c_d.DEPART_TXT,
                                     str(dep.name))

        page = HtmlGen(os.path.join(dir_man.g_dir_man.output_orders_dir, item_dir_name), item_file_name)

        WebGenerator.__gen_page_head(page, dev_str, c_d.LEVEL_UP * 3)
        WebGenerator.__gen_content_start(page)
        WebGenerator.__gen_table_head(page)

        WebGenerator.__gen_items_table_head(page,
                                    [dev_str, dep_str])

        WebGenerator.__gen_items_content(page, dep, items)

        WebGenerator.__gen_table_foot(page)
        WebGenerator.__gen_back_link(page)
        WebGenerator.__gen_content_end(page)
        WebGenerator.__gen_page_foot(page)

        page.close()

        logger.info("finish gen item page: {:s}".format(str(device_selector_id)))

    @staticmethod
    def __gen_soft_type_typyle(soft_type, domain):
        domain_title = domain.strip(".")
        if domain_title:
            return "{:s} : {:s}".format(soft_type, domain_title)
        else:
            return soft_type

    @staticmethod
    def __gen_items_content(page, dep, items):
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
                    type_class_id = WebGenerator.__change_class_type(type_class_id)

            page.w_o_tag(h_d.T_TR,
                         h_d.A_CLASS.format(type_class_id))

            # order soft type
            soft_type_class = h_d.A_CLASS.format(type_class_id
                                                 + " " + c_d.CL_TEXT_CENTER
                                                 + " " + c_d.CL_BORDER)
            repo_obj = dep.repos[item.repo_index][REPO_OBJECT]
            WebGenerator.__gen_item_soft_type(page,
                                              WebGenerator.__gen_soft_type_typyle(repo_obj.soft_type, item.solution_domain),
                                              soft_type_class)

            # tag date and commit hash
            WebGenerator.__gen_common_columns(page,
                                              repo_obj,
                                              dep.commits[item.commit_index],
                                              item,
                                              type_class_id)

            page.w_c_tag(h_d.T_TR)

    def __gen_device_content(self, file, model, dep_name, dev_name):
        dep = model.departments[dep_name]
        dev_items = [item for item in dep.items if item.device_class == dev_name]

        type_class_id = 0
        for type in c_d.TAG_DEVICE_SELECTORS:
            for tag_class in c_d.TAG_CLASSES:
                tag_class_index = c_d.TAG_CLASSES.index(tag_class)
                tag_class_i10n = c_d.TAG_CLASSES_I10N[tag_class_index]

                typed_items = [item for item in dev_items if item.device_selector_type == type and item.tag_class == tag_class]

                unic_nums = sorted([key for key in dict.fromkeys([item.device_selector_id for item in typed_items]).keys()],
                                   reverse=False)

                for num in unic_nums:
                    first_s_t = True
                    nummed_items = [item for item in typed_items if item.device_selector_id == num]

                    soft_type_by_num = []
                    sd_types = []
                    for n_item in nummed_items:
                        s_type = dep.repos[n_item.repo_index][REPO_OBJECT].soft_type
                        
                        if s_type not in soft_type_by_num:
                            soft_type_by_num.append(s_type)
                            
                        d_type = n_item.solution_domain
                        sd_type = s_type + ":" + d_type
                        if sd_type not in sd_types:
                            sd_types.append(sd_type)
                            

                    for soft_t in dep.soft_types:
                        s_typed_items = [item for item in nummed_items if dep.repos[item.repo_index][REPO_OBJECT].soft_type == soft_t]

                        if not s_typed_items:
                            continue

                        pre_ld_item = max(s_typed_items, key=lambda item: item.tag_date)
                        is_concrete_device_item = pre_ld_item.device_selector_type != c_d.TAG_DEVICE_SELECTOR_TYPE_ALL
                        if is_concrete_device_item:
                            domains = [pre_ld_item.solution_domain]
                        else:
                            for n_item in nummed_items:
                                new_domain = n_item.solution_domain
                                if new_domain not in domains:
                                    domains.append(new_domain)
                            domains = sorted(domains)

                        for domain in domains:

                            d_typed_items = [item for item in s_typed_items if
                                             item.solution_domain == domain]

                            if not d_typed_items:
                                continue

                            ld_item = max(d_typed_items, key=lambda item: item.tag_date)

                            type_class_id_str = c_d.CL_TD_INC.format(str(type_class_id))

                            file.w_o_tag(h_d.T_TR,
                                         h_d.A_CLASS.format(str(type_class_id)) +
                                         h_d.A_ON_MOUSE_OVER.format(c_d.CALC_METRICS_FUNC) +
                                         h_d.A_ON_MOUSE_OUT.format(c_d.CALC_DEF_METR_FUNC))

                            # order num
                            if first_s_t:
                                first_s_t = False
                                title = WebGenerator.__get_num_by_type(ld_item.device_selector_type, ld_item.device_selector_id)
                                if ld_item.device_selector_type == c_d.TAG_DEVICE_SELECTOR_TYPE_ALL:
                                    title = tag_class_i10n + title

                                order_link_attrs = (title,
                                                    WebGenerator.join_path(
                                                        c_d.OUTPUT_DEVICE_ORDERS_REL_DIR,
                                                        WebGenerator.__get_item_dir_name(dev_name, ld_item.device_selector_id),
                                                        WebGenerator.__get_item_file_name(dev_name, ld_item.device_selector_id)),
                                                    h_d.A_TITLE.format(c_d.CNT_TXT + str(len(nummed_items))))

                                if is_concrete_device_item:
                                    rows_span = len(soft_type_by_num)
                                else:
                                    rows_span = len(sd_types)
                                
                                WebGenerator.__gen_order_num(file,
                                                             h_d.A_CLASS.format(type_class_id_str
                                                                                + " " + c_d.CL_TD_NUM
                                                                                + " " + c_d.CL_BORDER)
                                                             + h_d.A_ROWSPAN.format(str(rows_span)),
                                                             [order_link_attrs])

                            # order soft type
                            soft_type_class = h_d.A_CLASS.format(type_class_id_str
                                                             + " " + c_d.CL_TEXT_CENTER
                                                             + " " + c_d.CL_BORDER)

                            WebGenerator.__gen_item_soft_type(file,
                                                              WebGenerator.__gen_soft_type_typyle(soft_t, domain),
                                                              soft_type_class)

                            # tag date and commit hash
                            repo = dep.repos[ld_item.repo_index][REPO_OBJECT]
                            commit = dep.commits[ld_item.commit_index]
                            WebGenerator.__gen_common_columns(file,
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

    @staticmethod
    def __gen_common_columns(file, repo, commit, item, type_class_id):
        column_class = h_d.A_CLASS.format(type_class_id
                                          + " " + c_d.CL_TEXT_LEFT
                                          + " " + c_d.CL_BORDER)
        # tag date
        WebGenerator.__gen_tag_date(file,
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
                       h_d.A_TITLE.format(WebGenerator.__get_title_for_commit(repo.link, commit.auth,
                                                                              commit.date, commit.msg)))

        links_list.append(repo_link_c)

        ver_class = h_d.A_CLASS.format(type_class_id
                                       + " " + c_d.CL_TD_VER
                                       + " " + c_d.CL_BORDER)

        if item.device_selector_type is c_d.TAG_DEVICE_SELECTOR_TYPE_ALL:
            ftp_link_c = (c_d.REDIST_TXT,
                          WebGenerator.form_dist_link(commit, repo),
                          h_d.A_TITLE.format(c_d.LINK_FTP_TXT)
                          + h_d.A_TARGET.format(h_d.A_TARGET_BLANK))
            links_list.append(ftp_link_c)

        WebGenerator.__gen_tag_commit_version(file,
                                              ver_class,
                                              links_list)

        metr_class = h_d.A_CLASS.format(type_class_id
                                        + " " + c_d.CL_TEXT_RIGHT
                                        + " " + c_d.CL_BORDER)
        WebGenerator.__gen_metrics_column(file, metr_class, item.metric)

    @staticmethod
    def __gen_metrics_column(gen, cl, metric):
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

    @staticmethod
    def __change_class_type(c_type):
        if c_type == c_d.CL_TD_1:
            c_type = c_d.CL_TD_2
        elif c_type == c_d.CL_TD_2:
            c_type = c_d.CL_TD_1

        return c_type

    @staticmethod
    def __gen_back_link(gen):
        gen.w_o_tag(h_d.T_P, h_d.A_CLASS.format(c_d.CL_FOOT_BACK), True)
        gen.w_tag(h_d.T_A,
                  c_d.BACK_TXT,
                  h_d.BLK_ONCLICK_BACK)
        gen.w_c_tag(h_d.T_P)

    @staticmethod
    def __gen_device_head_tooltip():
        tooltip = ""

        return tooltip

    @staticmethod
    def __gen_device_table_head(gen, text_list, tooltip):
        WebGenerator.__gen_top_dev_order_table_head(gen, text_list, tooltip, c_d.D_TABLE_COLSPAN)
        WebGenerator.__gen_mid_table_head(gen)
        WebGenerator.__gen_mid_table_mid(gen)
        WebGenerator.__gen_mid_common_table_body(gen)
        WebGenerator.__gen_mid_table_foot(gen)
        WebGenerator.__gen_bottom_table_head(gen)

    @staticmethod
    def __gen_items_table_head(gen, text_list):
        WebGenerator.__gen_top_dev_order_table_head(gen, text_list, "", c_d.M_TABLE_CS_ITEM)
        WebGenerator.__gen_mid_table_head(gen)
        WebGenerator.__gen_mid_common_table_body(gen)
        WebGenerator.__gen_mid_table_foot(gen)
        WebGenerator.__gen_bottom_table_head(gen)

    @staticmethod
    def __gen_top_dev_order_table_head(gen, text_list, title, span):
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

    @staticmethod
    def __get_item_file_name(name, num):
        return "{:s}_{:s}{:s}".format(name, str(num), c_d.HTML_EXT)

    @staticmethod
    def __get_item_dir_name(name, num):
        return "{:s}_{:s}".format(name, str(num))

    @staticmethod
    def __get_device_file_name(name):
        return "{:s}{:s}".format(name, c_d.HTML_EXT)

    @staticmethod
    def __get_title_for_commit(repo, author, commDate, commMsg):
        return c_d.REPO_TXT + repo + "\n" \
               + c_d.AUTHOR_TXT + author + "\n" \
               + c_d.COMM_DATE_TXT + commDate + "\n" \
               + c_d.COMM_MSG_SH_TXT.format(commMsg)

    def __set_current_timestamp(self):
        self.__cur_timestamp = datetime.datetime.now().strftime(c_d.TYPICAL_TIMESTAMP)

    @log_func_name(logger)
    def generate_web(self, model, partly_update):
        self.__set_current_timestamp()

        if not partly_update:
            WebGenerator.__clear_out_dir(dir_man.g_dir_man.output_dir)
            WebGenerator.__gen_read_metrics_help_page()

        self.__gen_index(model)
        self.__gen_pages(model)

