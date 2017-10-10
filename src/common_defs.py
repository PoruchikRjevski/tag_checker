import global_vars as g_v

# WEB_GEN -----------------------------------------------------------
DEVICE_DIR          = "devices/"
DEVICE_PATH         = g_v.OUT_PATH + DEVICE_DIR
ORDERS_DIR          = "orders/"
ORDERS_PATH         = DEVICE_PATH + ORDERS_DIR
FILE_EXT            = ".html"

LEVEL_UP            = "../"

JS_DIR              = "js"
CSS_DIR             = "css"

STYLE_F_NAME        = "style.css"
SCRIPTS_F_NAME      = "scripts.js"
JS_METRICS_F_NAME   = "metrics.js"

CL_MAIN_TABLE       = "main_table"
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
CL_BORDER           = "border"
CL_MAIN_HEAD        = "main_head"
CL_MID_HEAD         = "mid_head"
CL_IFRAME           = "main_frame"
CL_BACK_CIRLE       = "back_circle"

DATE_ATR_ORDINAL    = "ordinal"

D_TABLE_COLSPAN     = "4"
M_TABLE_COLSPAN     = "2"
M_TABLE_CS_ITEM     = "3"
MID_ROWS            = "2"
DEV_MID_ROWS        = "3"
BTM_ROWS            = "1"
M_TABLE_H_NUM       = "2"

MAIN_F_NAME         = "main.html"
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
LINK_TO_FTP         = "ftp://172.16.20.64/redist/bourevestnik.ru/{:s}/{:s}" # :0 - device name,
                                                                            # :1 - commit hash
GW_SHORTLOG         = "shortlog"
GW_COMMIT           = "commit"

# footer
LAST_UPD_TXT        = "Последнее обновление: "
CR_TXT              = "&copy;140 отдел. Буревестник."
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

VER_TXT             = "Версия: {:s}.{:s}.{:s}({:s}) {:s}"

REPOS_NUM_TXT       = "Репозиторев: {:s}"
TAGS_NUM_TXT        = "Всего тэгов: {:s}"
PROC_TAGS_NUM_TXT   = "Обработанных тэгов: {:s}"
SCAN_TIME_TXT       = "Общее время обработки: {:s}"
LAST_AUTH_TXT       = "Последний коммитер: {:s}"

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

E_GNT_STR           = "Git not installed"
E_CFNE_STR          = "Config file does not exist"
E_BAD_ARGS          = "Bad arguments"

# CFG LOADER --------------------------------------------------------
BLOCK_CONFIG        = "CONFIG"
BLOCK_TRAN          = "TRANSLATE"
SECT_REPOS          = "repos"
SECT_PREFIX         = "prefix"
SECT_PAIRS          = "pairs"
OUT_P               = "out"

CFG_F_NAME          = "tag_checker.ini"

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
PROD                = ("PROD", "ROD")
WRONG_NUM           = ("xxxx", "XXXX")

TYPE_ITEM           = "ITEM"
TYPE_ORDER          = "ORDER"
TYPE_ALL            = "ALL"

TYPES_L             = [TYPE_ITEM, TYPE_ORDER, TYPE_ALL]

D_UNK               = "UNKNOWN"
D_LINUX               = "LINUX"
D_WIN               = "WIN"
D_DOS               = "DOS"

DOMENS_L            = [D_LINUX, D_WIN, D_DOS]

# PLATFORMS ---------------------------------------------------------
WINDOWS_P           = "windows"
LINUX_P             = "linux"

LIN_OUT_P_DEF       = "/var/www/swver_hist/"
WIN_OUT_P_DEF       = "../out/"

WIN_LOG_P_DEF       = "../log/"
LIN_LOG_P_DEF       = "/tmp/tag_checker_log/"

LIN_CFG_P           = "/etc/"
WIN_CFG_P           = "../cfg/"

# CMD WRAP ----------------------------------------------------------
SUDO_CMD            = "sudo "

# OTHER -------------------------------------------------------------
REPO_SUFFIX         = ".git"
DOC_CODE            = "utf-8"