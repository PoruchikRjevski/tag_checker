# constants for checker

__doc__ = "First argument it is the path to config.ini"

CHECKER = "checker"
CMD_WRAP = "cmd_wrap"

EXIT_NORMAL     = 0             # all ok
EXIT_GNT        = 1             # git not installed
EXIT_WA         = 2             # wron arguments
EXIT_CFNE       = 4             # config file does not exist

E_GNT_STR       = "Git not installed"
E_CFNE_STR      = "Config file does not exist"
E_WA_STR        = "Wrong arguments"
FOR_HELP        = "for help use --help"