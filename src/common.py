# constants for checker
TAG_CHECKER     = "tag_checker"

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