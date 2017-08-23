# constants for checker
TAG_CHECKER     = "tag_checker"
REPOS           = "repos"

# tag model
PROD            = ("PROD", "ROD")

TYPE_ITEM       = "ITEM"
TYPE_ORDER      = "ORDER"
TYPE_ALL        = "ALL"

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
GET_COMM_DATE   = "git show -s --format=%ci "               # get commit date by hash

QUIET           = False                                     # global flag for out or not log and err messages
CUR_PLATFORM    = "None"
CUR_PATH        = "None"

LOG_T           = "LOG"
ERR_T           = "ERR"

# platforms
WINDOWS_P       = "windows"
LINUX_P         = "linux"

WIN_PATH        = "../log/"
LIN_PATH        = "/tmp/tag_checker_log/"

# tag descr
ORDER           = "PROD"
DEVICE          = "APP"
ITEM            = "ITEM"

# web generator
INDEX_PATH      = "../out/"
INDEX_NAME      = "index.html"
FILE_EXT        = ".html"

BORDER_WIDTH    = "1"
TABLE_WIDTH     = "100%"
TABLE_COLOR     = "#aaaaaa"
CELLPADDING     = "10%"
FONT_FAM        = "arial"
FONT_SZ         = "13"
ALIGN           = "center"

DOC_CODE        = "utf-8"

TABLE_HD_COL    = "#cccccc"
TABLE_TR_COL_1  = "#eeeeee"
TABLE_TR_COL_2  = "#dddddd"
MAIN_TABLE_COLS = "5"
MID_ROWS        = "2"
BTM_ROWS        = "1"

# page table header
MAIN_HEAD       = "Актуальные прошивки"
DEPARTMENT      = "Отдел"
DEVICE          = "Устройство"
ITEM            = "№"
LAST_SET        = "Последняя установка"
DATE            = "Дата установки"
HASH            = "Хэш-сумма коммита(дата)"
HISTORY         = "История прошивок для устройства - "

# page table content
FOR_ALL         = "для всех"
ITEM_NUM        = "Зав. № "
ORDER_NUM       = "Заказ "

# back link
BACK            = "Назад"