# constants for checker

CHECKER = "checker"
CMD_WRAP = "cmd_wrap"

EXIT_NORMAL     = 0             # all ok
EXIT_GNT        = 1             # git not installed
EXIT_WA         = 2             # wron arguments
EXIT_CFNE       = 4             # config file does not exist

E_GNT_STR       = "Git not installed"
E_CFNE_STR      = "Config file does not exist"
E_WA_STR        = "Wrong arguments"
FOR_HELP        = "For help use --help"

# git answers
BR_DEV          = "develop"

# git commands
CUR_BRANCH      = "git branch" # get current branch
SW_BRANCH       = "git checkout " # switch to develop
CD_TO           = "cd " # cd to TODO for win