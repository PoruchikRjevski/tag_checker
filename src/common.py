# constants for checker
TAG_CHECKER     = "tag_checker"
REPOS           = "repos"
PREFIX          = "prefix"
CONFIG          = "CONFIG"
OUT_P           = "out"
TRANSLATE_PATH  = "translate"

CONFIG_PATH     = "/etc/tag_checker.ini"
TRANSLATE_PATH  = "/etc/tag_checker_translate"

OUT_PATH_DEF    = "/var/www/swver_hist/"

LOG_SYMB_CALLER = 40

# tag model
PROD            = ("PROD", "ROD")

TYPE_ITEM       = "ITEM"
TYPE_ORDER      = "ORDER"
TYPE_ALL        = "ALL"

TYPES_L = [TYPE_ITEM, TYPE_ORDER, TYPE_ALL]

# exit codes and outputs
EXIT_NORMAL     = 0                                         # all ok
EXIT_GNT        = 1                                         # git not installed
EXIT_WA         = 2                                         # wron arguments
EXIT_CFNE       = 4                                         # config file does not exist

E_GNT_STR       = "Git not installed"
E_CFNE_STR      = "Config file does not exist"
E_WA_STR        = "Wrong arguments"
FOR_HELP        = "For help use --help"

# git answers
BR_DEV          = "develop"
BR_ORIG         = "original"

# git commands
GIT_VER         = "git --version"                           # get git ver
CUR_BRANCH      = "git rev-parse --abbrev-ref HEAD"         # get current branch
SW_BRANCH       = "git checkout "                           # switch branch to
UPD_REPO        = "git pull"                                # update repo
GET_TAGS        = "git tag"                                 # get all tags for cur branch
GET_TAG_SSHA    = "git rev-parse --short "                  # get short SHA1 for tagged commit
GET_COMM_DATE   = "git show -s --format=%cd --date=short "  # get commit date by hash
GET_COMM_INFO   = "git log -{0!s} --format='{1!s}' "        # get commit info
FORM_AUTHOR     = "%ae"                                     # author
FORM_PAR_SHASH  = "%p"                                      # parents hash

GIT_PAR_SH_NEST = 10
GIT_AUTHOR_NEST = 1

QUIET           = False                                     # global flag for out or not log and err messages
LOGGING         = False                                     # global flag for out or not log and err to files
SUDOER          = False                                     # global flag for exec shell cmd by sudo
CUR_PLATFORM    = "None"
CUR_PATH        = "None"

LOG_T           = "LOG"
ERR_T           = "ERR"

# platforms
WINDOWS_P       = "windows"
LINUX_P         = "linux"

WIN_PATH        = "../log/"
LIN_PATH        = "/tmp/tag_checker_log/"

SUDO_CMD        = "sudo "

# tag descr
ORDER           = "PROD"
DEVICE          = "APP"
ITEM            = "ITEM"

# web generator
OUT_PATH        = ""
INDEX_NAME      = "index.html"
MAIN_NAME       = "main.html"
DEVICE_DIR      = "devices/"
DEVICE_PATH     = OUT_PATH + DEVICE_DIR
ORDERS_DIR      = "orders/"
ORDERS_PATH     = DEVICE_PATH + ORDERS_DIR
FILE_EXT        = ".html"
LEVEL_UP        = "../"
SCRIPTS_NAME    = "js_scripts.js"

BORDER_WIDTH    = "1"
TABLE_WIDTH     = "100%"
TABLE_COLOR     = "#aaaaaa"
CELLPADDING     = "5%"
FONT_FAM        = "arial"
FONT_SZ         = "12"
ALIGN           = "center"
BLACK           = "black"
WHITE           = "white"

DOC_CODE        = "utf-8"

MAIN_T_HD_COL   = "#333333"
TABLE_HD_COL    = "#555555"
TABLE_TR_COL_1  = "#eeeeee"
TABLE_TR_COL_2  = "#dddddd"
MAIN_TABLE_COLS = "5"
MID_ROWS        = "2"
BTM_ROWS        = "1"

FRAME_ID        = "pridurok"
FRAME_POS       = "absolute"
FRAME_BORDER    = "none"
FRAME_H         = "100%"
FRAME_W         = "100%"


# page table header
MAIN_HEAD       = "Актуальные прошивки"
DEPARTMENT      = "Отдел"
DEVICE          = "Устройство"
ITEM            = "№"
LAST_SET        = "Последняя установка"
DATE            = "Дата установки"
HASH            = "Хэш-сумма коммита(дата)"
HISTORY         = "История прошивок для устройства "

# page table content
FOR_ALL         = "для всех"
ITEM_NUM        = "Зав. № "
ORDER_NUM       = "Заказ "

# back link
BACK            = "На главную"

# footer
LAST_UPD        = "Последнее обновление: "
AUTHOR          = "140 отдел. Буревестник."