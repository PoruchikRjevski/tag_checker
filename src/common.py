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
E_MANY_OPT      = "Too many options"
E_MANY_ARG      = "Too many arguments"
E_FEW_OPT       = "Too few options"
E_FEW_ARG       = "Too few arguments"