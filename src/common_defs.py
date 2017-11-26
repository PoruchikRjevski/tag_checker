import os
import global_vars as g_v

# WEB_GEN -----------------------------------------------------------
OUTPUT_DEVICE_REL_DIR          = "devices/"
OUTPUT_DEVICE_ORDERS_REL_DIR   = "orders/"
HTML_EXT            = ".html"

LEVEL_UP            = "../"

JS_DIR              = "js"
CSS_DIR             = "css"

STYLE_F_NAME        = "style.css"
SCRIPTS_F_NAME      = "scripts.js"
JS_METRICS_F_NAME   = "metrics.js"

CL_MAIN_TABLE       = "main_table"
CL_HELP_TABLE       = "help_table"
CL_FOOT_INFO        = "foot_info"
CL_FOOT_BACK        = "foot_back"
CL_WRAPPER          = "wrapper"
CL_CONTENT          = "content"
CL_FOOTER           = "footer"
CL_MT_H             = "mt_head"
CL_MT_F             = "mt_foot"
CL_TR_1             = "tr_1"
CL_TD_1             = "td_1"
CL_TD_2             = "td_2"
CL_TD_INC           = "td_inc_{:s}"
CL_TD_VER           = "version"
CL_TD_NUM           = "num"
CL_TEXT_CENTER      = "t_center"
CL_TEXT_RIGHT       = "t_right"
CL_TEXT_LEFT        = "t_left"
CL_BORDER           = "border"
CL_MAIN_HEAD        = "main_head"
CL_MID_HEAD         = "mid_head"
CL_IFRAME           = "main_frame"
CL_BACK_CIRLE       = "back_circle"
CL_GREEN_BGRND      = "green"
CL_RED_BGRND        = "red"
CL_YELLOW_BGRND     = "yellow"
CL_WHITE_TXT        = "txt_white"
CL_NO_WRAP          = "no_wrap"
CL_BLACK_TEXT       = "black_text"

CL_CIRCLE           = "circle"
CL_BAGEL_BLUE       = "bagel_blue"
CL_BAGEL_GREEN      = "bagel_green"

CLR_GREEN_TXT       = "Текущая версия"
CLR_GREEN_BAGEL_TXT = "Форсированная до текущей базовой версия"
CLR_RED_TXT         = "Старая версия"
CLR_YEL_TXT         = "Форсированная старая версия"
CLR_BLUE_TXT        = "Экспериментальная версия"
CLR_BLUE_BAGEL_TXT  = "Отмененная экспериментальная версия"

CLR_BLUE            = 0x96b0ff#0x3f3fff

CLR_BLUE_MAX        = 0xa5adff
CLR_BLUE_MIN        = 0x4149ff
CLR_BLUE_STEP       = 0x10100
CLR_BLUE_STEPS      = (CLR_BLUE_MAX - CLR_BLUE_MIN) / CLR_BLUE_STEP #100 steps

CLR_GREEN           = 0x1fe800#b2fca6#0x3fef3f

CLR_RED_MAX         = 0xffc3c3#fff0f0
CLR_RED_MIN         = 0xff0f0f#ff0f0f
CLR_RED_STEP        = 0x000101
CLR_RED_STEPS      = (CLR_RED_MAX - CLR_RED_MIN) / CLR_RED_STEP #100 steps 180 - b4b4

CLR_YEL             = 0xede500

DATE_ATR_ORDINAL    = "ordinal"

H_TABLE_CS          = "3"
D_TABLE_COLSPAN     = "5"
M_TABLE_COLSPAN     = "2"
M_TABLE_CS_ITEM     = "4"
MID_ROWS            = "2"
DEV_MID_ROWS        = "3"
BTM_ROWS            = "1"
M_TABLE_H_NUM       = "2"

MAIN_F_NAME         = "main.html"
HELP_METR_F_NAME    = "how_to_read_metrics.html"
INDEX_F_NAME        = "index.html"

CALC_METRICS_FUNC   = "calcTimeMetrics(this);"
CALC_DEF_METR_FUNC  = "calcDefTimeMetrics();"

FRAME_ID            = "includer"
FRAME_POS           = "absolute"
FRAME_BORDER        = "none"
FRAME_H             = "100%"
FRAME_W             = "100%"
FRAME_NOT           = "Bad browser"

ALIGN_C             = "center"
ALIGN_R             = "right"
ALIGN_L             = "left"

TABLE_CELLPAD       = "5%"

FRAME_BAD_NAME      = "BAD_FRAME_NAME"

# links
LINK_TO_SRC_REPO    = "http://172.16.20.64/swver_hist/gitweb/?p=opensource/device_tag_visualiser.git;a={:s};ch={:s};h={:s}"

LINK_TO_REPO        = "http://172.16.20.64/swver_hist/gitweb/?p=bourevest/{:s};a={:s};ch={:s};h={:s}"   # :0 - repo name
                                                                                                        # :1 - out type
                                                                                                        # :2 - commit hash for select
                                                                                                        # :3 - hash of parrent commit
GW_SHORTLOG         = "shortlog"
GW_COMMIT           = "commit"

# footer
LAST_UPD_TXT        = "Последнее обновление: "
CR_TXT              = "&copy; 2017 - 140 отдел. Буревестник."
M_HEAD_TXT          = "Актуальные прошивки"
DEP_TXT             = "Отдел"
DEV_TXT             = "Прибор"
ITEM_TXT            = "№"
SOFT_TYPE_TXT       = "Тип"
LAST_SET_TXT        = "Последняя установка"
DATE_TXT            = "Дата установки"
HASH_TXT            = "Версия"
METRICS_TXT         = "Метрики"
TAG_TXT             = "Тэг: "
CNT_TXT             = "В истории: "
BACK_TXT            = "Назад"
LINK_FTP_TXT        = "Ссылка на дистрибутив"
REDIST_TXT          = " [R]"
HISTORY_TXT         = "История прошивок для устройства "
DEPART_TXT          = "Отдел: "

TO_DEV_TXT          = "Перейти к списку приборов"
READ_METR_TXT       = "Расшифровка цветовых обозначений метрик"
CLRD_DESIGN_TXT     = "Цветовое обозначение"
TXT_DESIGN_TXT      = "Текстовое обозначение"
DESCRIPTION_TXT     = "Описание"

VER_TXT             = "Версия: {:s}.{:s}.{:s}({:s}) {:s}"

F_MULT_TXT          = "m"
F_LOG_TXT           = "l"
F_VERBOSE_TXT       = "v"
F_SUDO_TXT          = "s"
F_DEBUG_TXT         = "d"
F_TIMINGS_TXT       = "t"

REPOS_NUM_TXT       = "Репозиторев: {:s}"
TAGS_NUM_TXT        = "Всего тэгов: {:s}"
PROC_TAGS_NUM_TXT   = "Валидных тэгов: {:s}"
SCAN_TIME_TXT       = "Общее время обработки: {:s}"
LAST_AUTH_TXT       = "Последний коммитер: {:s}"
UPDATED_DEVS_TXT    = "Обновлены: {:s}"

REPO_TXT            = "Репозиторий: "
AUTHOR_TXT          = "Автор коммита: "
COMM_DATE_TXT       = "Дата коммита: "
COMM_MSG_SH_TXT     = "Сообщение коммита: {:s}"

T_FOR_ALL_TXT       = "Для всех"
T_ITEM_TXT          = "Зав.&nbsp;&nbsp;№&nbsp;"
T_ORDER_TXT         = "Заказ&nbsp;№&nbsp;"

# exit codes and outputs
EXIT_NORMAL         = 0                                         # all ok
EXIT_GNT            = 1                                         # git not installed
EXIT_WA             = 2                                         # wron arguments
EXIT_WO             = 3                                         # wrong options
EXIT_CFNE           = 4                                         # config file does not exist
EXIT_AR             = 5                                         # already run

E_GNT_STR           = "Git not installed"
E_CFNE_STR          = "Config file does not exist"
E_BAD_ARGS          = "Bad arguments"
E_ALREADY_RUNS      = "Already run's"

# CFG LOADER --------------------------------------------------------
BLOCK_CONFIG        = "CONFIG"
BLOCK_TRAN          = "TRANSLATE"
OPTION_REPOS          = "repos"
OPTION_PREFIX         = "prefix"
SECT_DIST_LINK_PATTERN = "dist_link_pattern"
SECT_DIST_LINK_PREFIX = "dist_link_prefix"
SECT_PAIRS          = "pairs"

CFG_OUTPUT_DIR_OLD_P = "out"
CFG_OUTPUT_DIR_P    = "out_dir"
CFG_ROOT_DIR_P      = "root_dir"
CFG_BIN_DIR_P       = "bin_dir"
CFG_CONFIG_DIR_P    = "cfg_dir"
CFG_DATA_DIR_P      = "data_dir"
CFG_LOGGER_DIR_P    = "log_dir"

CONFIG_FILE_NAME    = "config.ini"

# LOGGER
LOG_T               = "LOG"
ERR_T               = "ERR"

LOG_SYMB_CALLER     = 50
LOG_SYMB_C_LINE     = 5

# GIT MAN -----------------------------------------------------------
GIT_PAR_SH_NEST     = 15        # deep of seaching parents hash
GIT_AUTHOR_DEEP     = 1         # deep for searching commits info

COMMIT_MSG_SIZE     = 30        # edge for commit msg size

GIT_VER             = "version"

BAD_DATE            = "BAD DATE"

# TAG MODEL ---------------------------------------------------------
TAG_CLASSES         = ("PROD", "ROD", "TEST")  # TODO 1: what is "ROD", typo or for testing?
WRONG_NUM           = ("xxxx", "XXXX")

TAG_DEVICE_SELECTOR_TYPE_ITEM   = "ITEM"
TAG_DEVICE_SELECTOR_TYPE_SERIE  = "ORDER"
TAG_DEVICE_SELECTOR_TYPE_ALL    = "ALL"

TAG_DEVICE_SELECTORS = [TAG_DEVICE_SELECTOR_TYPE_ITEM, TAG_DEVICE_SELECTOR_TYPE_SERIE, TAG_DEVICE_SELECTOR_TYPE_ALL]

# PLATFORMS ---------------------------------------------------------
SOLUTION            = "tag_checker"
WINDOWS_P           = "windows"
LINUX_P             = "linux"

# CMD WRAP ----------------------------------------------------------
SUDO_CMD            = "sudo "

# OTHER -------------------------------------------------------------
REPO_SUFFIX         = ".git"
DOC_CODE            = "utf-8"
POST_RX_HOOK_NAME   = "post-receive"
HOOKS_PATH          = "hooks/"

GIT_HOOKS_PATH      = "misc/git-hooks/"
UPDATE_TABLE_FILE_NAME = "update.ini"

SECTION_UPD         = "UPDATE"
OPTION_UPD          = "to_update"

TYPICAL_TIMESTAMP   = "%Y-%m-%d %H:%M"

# LOGGER
LOG_TIME            = '%(asctime)s'
LOG_LEVEL           = '%(levelname)-8s'
LOG_THREAD          = '%(threadName)-15s'
LOG_FUNC            = '%(funcName)-30s'
LOG_LINE            = "%(lineno)-4d"
LOG_CALL            = '%(module)s:%(funcName)s():%(lineno)d'
LOG_MSG             = '%(message)s'
LOG_NAME            = '%(name)-30s'
