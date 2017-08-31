# constants for checker
TAG_CHECKER     = "tag_checker"
REPOS           = "repos"
PREFIX          = "prefix"
CONFIG          = "CONFIG"
OUT_P           = "out"
TRANSLATE_PATH  = "translate"

CONFIG_PATH     = "/etc/tag_checker.ini"
TRANSLATE_PATH  = "/etc/tag_checker_translate"


LINK_TO_REPO    = "http://172.16.20.64/swver_hist/gitweb/?p=bourevest/{:s};a={:s};cm={:s};h={:s}"
# http://172.16.20.64/gitweb/?p=bourevest/ase-2.git;a=shortlog;h=68b81e8557e56f63538e4ecff71cd84b9a5ba009

GW_SHORTLOG     = "shortlog"
GW_COMMIT       = "commit"

FILE_PREFIX     = "file://"

REPO_SUFFIX     = ".git"

OUT_PATH_DEF    = "/var/www/swver_hist/"

LOG_SYMB_CALLER = 40

# tag model
PROD            = ("PROD", "ROD")
WRONG_NUM       = ("xxxx", "XXXX")

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
GIT_VER         = "git --version"                                       # get git ver
CUR_BRANCH      = "git rev-parse --abbrev-ref HEAD"                     # get current branch
SW_BRANCH       = "git checkout {:s}"                                   # switch branch to
UPD_REPO        = "git pull"                                            # update repo
GET_TAGS        = "git tag"                                             # get all tags for cur branch
GET_TAG_SSHA    = "git rev-parse --short {:s}"                          # get short SHA1 for tagged commit
GET_COMM_DATE   = "git show -s --format=%cd --date=short {:s}"          # get commit date by hash
GET_COMM_INFO   = "git log {:s} -{:s} --format='{:s}' {:s}"             # get commit info
GET_PAR_COMM_H  = "git log --all --pretty=format:\"{:s}\" {:s}"         # parent hashes
GET_B_CONT      = "git branch --contains {:s}"                          # branch by hash
GET_LAST_COMM   = "git log -1 --pretty=format:\"{:s}\" {:s}"            # get last commit on branch
GET_LOG_BTW     = "git log --pretty=format:\"{:s}\" {:s} ^{:s}^ {:s}"   # get list of hashes between commits with tail
GET_REVL_BTW    = "git rev-list --abbrev-commit 1705ba3...3738f0c | tail -3"


GIT_CMD         = "git {:s}"
GIT_REV_LIST    = "rev-list {:s}"

FORM_AUTHOR     = "%ae"                                                 # author
FORM_PAR_SHASH  = "%p"                                                  # parents hash
FORM_PAR_SUBJ   = "%s"                                                  # commit msg
FORM_SHORT_HASH = "%h"
FORM_SINCE      = "--since=\"{:s}\" "                                   # git cmd since
FORM_TAIL       = " tail -{:s}"                                          # git tail
FORM_REVERSE    = "--reverse"
FORM_ALL        = "--all"
NO_MERGES       = "--no-merges "
ABBREV_COMM     = "--abbrev-commit "

GIT_PAR_SH_NEST = 15
GIT_AUTHOR_NEST = 1

COMMIT_MSG_SIZE = 30

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
ALIGN_C         = "center"
ALIGN_R         = "right"
BLACK           = "black"
WHITE           = "white"

DOC_CODE        = "utf-8"

MAIN_T_HD_COL   = "#333333"
TABLE_HD_COL    = "#555555"
TABLE_TR_COL_1  = "#eeeeee"
TABLE_TR_COL_2  = "#dddddd"
COLOR_STEP      = 0x101010
COLOR_TOP_EDGE  = 0xffffff
COLOR_BTM_EDGE  = 0x888888


MAIN_TABLE_COLS = "5"
MID_ROWS        = "2"
BTM_ROWS        = "1"

FRAME_ID        = "pridurok"
FRAME_POS       = "absolute"
FRAME_BORDER    = "none"
FRAME_H         = "99%"
FRAME_W         = "99%"


# page table header
MAIN_HEAD       = "Актуальные прошивки"
DEPARTMENT      = "Отдел"
DEVICE          = "Устройство"
ITEM            = "№"
LAST_SET        = "Последняя установка"
DATE            = "Дата установки"
HASH_STR            = "Хэш-сумма"
HISTORY         = "История прошивок для устройства "
DEPART_STR      = "Отдел: "

# page table content
FOR_ALL         = "для всех"
ITEM_NUM        = "Зав. № "
ORDER_NUM       = "Заказ "

# back link
BACK            = "На главную"

# footer
LAST_UPD        = "Последнее обновление: "
COPYRIGHT       = "&copy;140 отдел. Буревестник."
REPO_STR        = "Репозиторий: "
AUTHOR_STR      = "Автор коммита: "
TAG_STR         = "Тэг: "
CNT_STR         = "В истории: "
COMM_DATE_STR   = "Дата коммита: "
COMM_MSG_SHORT  = "Сообщение коммита: {:s}"
