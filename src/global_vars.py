QUIET               = False        # global flag for out or not log and err messages
LOGGING             = False         # global flag for out or not log and err to files
SUDOER              = False         # global flag for exec shell cmd by sudo
MULTITH             = False         # global flag for exec by multithreading
DEBUG               = False
TIMEOUTS            = False

OUT_PATH            = ""

DIST_LINK_PREFIX    = "ftp://172.16.20.64/bourevestnik.spb.ru/software/archive/"
DIST_LINK_PATTERN   = "${dist_prefix}%5B${sw_module_id}%5D.MOD/%5B${sw_module_version_id}%5D.VER"

CUR_PLATFORM        = None

CUR_PATH            = ""

SCAN_TIME           = ""
REPOS_NUM           = 0
TAGS_NUM            = 0
PROC_TAGS_NUM       = 0