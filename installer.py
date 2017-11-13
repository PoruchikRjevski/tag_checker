#!/usr/bin/sudo python3

import os
import sys
import time
import subprocess
import datetime
import curses
from filecmp import dircmp

# INSTALLER COMMON
DOC_CODE                    = "utf-8"


# INSTALLER DEFS
SOLUTION_NAME               = "tag_checker"
OUT_LOG_DIR                 = "/tmp/{:s}_log/".format(SOLUTION_NAME)
SETUP_DIR                   = "/opt/{:s}/".format(SOLUTION_NAME)
OUT_DIR                     = "/var/www/swver_hist/"
OUT_DEV_DIR                 = os.path.join(OUT_DIR, "devices/")
OUT_ORD_DIR                 = os.path.join(OUT_DEV_DIR, "orders/")
BACKUP_DIR                  = "/tmp/{:s}_backups/".format(SOLUTION_NAME)
CSS_DIR                     = "css/"
JS_DIR                      = "js/"
OUT_JS_DIR                  = os.path.join(OUT_DIR, JS_DIR)
OUT_CSS_DIR                 = os.path.join(OUT_DIR, CSS_DIR)
SRC_DIR                     = os.path.join(os.getcwd(), "src/")
MISC_DIR                    = "misc/"
CONFIG_NAME                 = "config"
CONFIG_EXT                  = ".ini"
CONFIG_DIR                  = "/etc/{:s}/".format(SOLUTION_NAME)
CONFIG_FILE                 = "{:s}{:s}".format(CONFIG_NAME,
                                                CONFIG_EXT)
CONFIG_EXMPL_DIR            = "config.example/"
LINK_PATH                   = "/usr/local/bin/"

MAIN_FILE                   = "main.py"
RUN_HELPER_FILE             = "run_helper.py"

EXEC_FILE                   = "run.sh"

VERSION_FILE                = "version.py"

UPDATE_ATTR                 = {"--update": "* * * * *"}
UPDATE_FULLY_ATTR           = {"--update --fully": "0 0 * * *"}


# CURSES MAIN MENU
HIGHLIGHT = None
NORMAL = None

SCREEN = None

M_INSTALL                   = "Install"
M_UNINSTALL                 = "Uninstall"
M_UPDATE_FILES              = "Update Files"
M_CHANGE_PARAMS             = "Change run parameters"
M_RESTORE_CFG               = "Backups"
M_EXIT                      = "Exit"

MAIN_M = [M_INSTALL, M_UNINSTALL, M_UPDATE_FILES, M_CHANGE_PARAMS, M_RESTORE_CFG, M_EXIT]
MAIN_M_SZ = len(MAIN_M)

HEAD_TXT                    = "Tag checker installer"
MENU_NAME_TXT               = "Menu"
CREATING_DIRS_TXT           = "Creating dirs"
REMOVING_DIRS_TXT           = "Removing dirs"
COPYING_TXT                 = "Copying"
REMOVING_TXT                = "Removing"
CREATE_EXEC_TXT             = "Create executable"
CREATE_LN_TXT               = "Create symlink"
REMOVE_LN_TXT               = "Remove symlink"
RESTORE_BACKUP_TXT          = "Backups"
REMOVE_BACKUP_TXT           = "Remove backup"
ADD_CRONTAB_TXT             = "Add task to crontab"
REM_CRONTAB_TXT             = "Remove task from crontab"


# CURSES PARAMS MENU
PARAMS_MENU_NAME_TXT        = "Select parameters"

M_P_VERBOSE                 = "Verbose"
M_P_V                       = "-v"
M_P_LOG                     = "Logging"
M_P_L                       = "-l"
M_P_MULTITHR                = "Multithreading"
M_P_MT                      = "-m"

PARAMS_MENU_STATE = {M_P_LOG:       [0, False, M_P_L],
                     M_P_MULTITHR:  [1, False, M_P_MT],
                     M_P_VERBOSE:   [2, False, M_P_V]}

PARAMS_MENU_SZ = len(PARAMS_MENU_STATE)


# CURSES OTHER
PROGRESS_BAR = None

KEY_RETURN                  = 10
KEY_SPACE                   = 32
KEY_DELETE                  = 330
KEY_ESC                     = 27

HEAD_TXT_SZ = len(HEAD_TXT) // 2

HEAD_HEIGHT                 = 2
NAME_HEIGHT                 = 4
BODY_HEIGHT                 = 6
SCROLLBAR_HEIGHT            = 10
CUR_WIDTH                   = 0

BACKUPS_MENU_NAME_TXT       = "Select backup"
CONFIDENCE_MENU_NAME_TXT    = "Are you sure?"


def screen_height_update(func):
    def wrapped(*args, **kwargs):
        global SCREEN
        global CUR_WIDTH

        _, width = SCREEN.getmaxyx()

        CUR_WIDTH = (width // 2) - HEAD_TXT_SZ

        return func(*args, **kwargs)
    return wrapped


def add_scrollbar(func):
    def wrapped(*args, **kwargs):
        global PROGRESS_BAR
        global SCROLLBAR_HEIGHT
        global CUR_WIDTH

        PROGRESS_BAR = curses.newwin(2, 20, SCROLLBAR_HEIGHT, CUR_WIDTH)
        PROGRESS_BAR.border(0)

        func(*args, **kwargs)
    return wrapped


def screen_refresh(func):
    def wrapped(*args, **kwargs):
        global CUR_WIDTH

        SCREEN.clear()
        SCREEN.border(0)

        SCREEN.addstr(HEAD_HEIGHT, CUR_WIDTH + 2, HEAD_TXT, curses.A_STANDOUT | curses.A_BOLD)

        func(*args, **kwargs)

        time.sleep(0.01)

        SCREEN.refresh()
    return wrapped


@screen_height_update
@screen_refresh
def show_confidence_menu():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, CONFIDENCE_MENU_NAME_TXT, curses.A_BOLD)

    SCREEN.addstr(BODY_HEIGHT + 2, CUR_WIDTH + 2,
                  "ENTER - OK, ESC - Cancel", NORMAL)


def check_confidence(func):
    def wrapped(*args, **kwargs):
        show_confidence_menu()

        key = get_key()

        if key == curses.KEY_ENTER or key == KEY_RETURN:
            return func(*args, **kwargs)

    return wrapped


def check_existence_strong(func):
    def wrapped(arg, *argv):
        if not os.path.exists(arg):
            true_exit(1, "{:s} not exist. Try to execute install.".format(arg))

        return func(arg, *argv)

    return wrapped


def check_existence_weak(func):
    def wrapped(arg, *argv):
        if os.path.exists(arg):
            return func(arg, *argv)

    return wrapped


@screen_refresh
def create_dir(path):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, CREATING_DIRS_TXT, curses.A_BOLD)

    if not os.path.exists(path):
        os.makedirs(path)
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Create dir: {:s}".format(path), NORMAL)
    else:
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Dir already exist: {:s}".format(path), NORMAL)


@screen_refresh
def remove_dir(path):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, REMOVING_DIRS_TXT, curses.A_BOLD)

    if os.path.exists(path):
        rm_dir(path)
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Remove dir: {:s}".format(path), NORMAL)
    else:
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Dir already removed: {:s}".format(path), NORMAL)


@screen_height_update
def create_dirs():
    create_dir(SETUP_DIR)
    create_dir(OUT_ORD_DIR)
    create_dir(OUT_CSS_DIR)
    create_dir(OUT_JS_DIR)
    create_dir(OUT_LOG_DIR)
    create_dir(CONFIG_DIR)
    create_dir(BACKUP_DIR)


@screen_height_update
def remove_dirs():
    remove_dir(SETUP_DIR)
    remove_dir(OUT_DIR)
    remove_dir(OUT_LOG_DIR)
    remove_dir(CONFIG_DIR)


def exec_cmd(cmd):
    proc = subprocess.Popen(['{:s}\n'.format(cmd)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)

    out, _ = proc.communicate()

    out = out.decode(DOC_CODE).strip()

    return out


@check_existence_weak
def cp_dir_star(src, dst):
    exec_cmd("yes | cp -rf {:s}* {:s}".format(src, dst))


@check_existence_weak
def cp_dir_dot(src, dst):
    exec_cmd("yes | cp -rf {:s}. {:s}".format(src, dst))


@check_existence_weak
def cp_file(src, dst=""):
    exec_cmd("cp -rfn {:s} {:s}".format(src, dst))


@check_existence_weak
def rm_dir(dst):
    exec_cmd("rm -rf {:s}".format(dst))


@check_existence_weak
def rm_file(dst):
    exec_cmd("rm -f {:s}".format(dst))


@check_existence_weak
def add_runnable_rights(dst):
    exec_cmd("chmod +x {:s}".format(dst))


@check_existence_weak
def create_ln(src, dst):
    exec_cmd("ln -s {:s} {:s}".format(src, dst))


@screen_refresh
def copy_source():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)
    cp_dir_star(SRC_DIR, SETUP_DIR)
    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Copy: {:s} to {:s}".format(SRC_DIR, SETUP_DIR), NORMAL)


@screen_refresh
def copy_misc():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)
    css_full_path = os.path.join(SRC_DIR, MISC_DIR, CSS_DIR)
    js_full_path = os.path.join(SRC_DIR, MISC_DIR, JS_DIR)

    cp_dir_dot(css_full_path, OUT_CSS_DIR)
    cp_dir_dot(js_full_path, OUT_JS_DIR)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Copy: {:s} to {:s}".format(SRC_DIR, SETUP_DIR), NORMAL)


@screen_refresh
def backup_config():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)

    create_dir(BACKUP_DIR)

    backup_dir = os.path.join(BACKUP_DIR,
                              "{:s}_{:s}/".format(SOLUTION_NAME,
                                                  datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

    last_backup = get_last_backup()

    do_backup = False

    if last_backup:
        if dircmp(os.path.join(BACKUP_DIR, "{:s}/".format(last_backup)), CONFIG_DIR).diff_files:
            do_backup = True
    else:
        do_backup = True

    if do_backup:
        cp_dir_dot(CONFIG_DIR, backup_dir)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Backup config: {:s}".format(CONFIG_FILE), NORMAL)


@screen_refresh
def copy_config():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)
    src_conf_dir = os.path.join(os.getcwd(),
                                CONFIG_EXMPL_DIR)

    cp_dir_star(src_conf_dir, CONFIG_DIR)
    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Copied: {:s} to {:s}".format(SRC_DIR, SETUP_DIR), NORMAL)


def create_exec_file(dst, link):
    with open(dst, 'w') as file:
        file.write('#!/bin/bash\n')
        file.write("{:s} {:s} $@".format(link,
                                         get_params_str()))
        file.flush()
        file.close()


@check_existence_weak
def read_exec_file_same_line_splitted(dst):
    same_line_splitted = []

    with open(dst, 'r') as file:
        same_line_splitted = file.read().split("\n")[1].split(" ")

        file.close()

    return same_line_splitted


@screen_refresh
def create_executable():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, CREATE_EXEC_TXT, curses.A_BOLD)

    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)
    run_helper_file = os.path.join(SETUP_DIR,
                                   RUN_HELPER_FILE)

    if not os.path.exists(SETUP_DIR) or not os.path.exists(run_helper_file):
        return

    create_exec_file(exec_file, run_helper_file)

    add_runnable_rights(exec_file)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Created executable: {:s}".format(exec_file), NORMAL)


@screen_refresh
def restore_cfg(backup_name):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, RESTORE_BACKUP_TXT, curses.A_BOLD)
    backup_path = os.path.join(BACKUP_DIR, "{:s}/".format(backup_name))

    cp_dir_star(backup_path, CONFIG_DIR)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Restored backup: {:s}".format(backup_name), NORMAL)


@screen_refresh
def create_symlink():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, CREATE_LN_TXT, curses.A_BOLD)

    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)

    symlink = os.path.join(LINK_PATH,
                           SOLUTION_NAME)

    create_ln(exec_file, symlink)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Created symlink: {:s}".format(symlink), NORMAL)


@screen_refresh
def remove_symlink():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, REMOVE_LN_TXT, curses.A_BOLD)

    symlink = os.path.join(LINK_PATH,
                           SOLUTION_NAME)

    rm_file(symlink)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Remove symlink: {:s}".format(symlink), NORMAL)


@screen_refresh
def add_to_crontab(attr_dict):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, ADD_CRONTAB_TXT, curses.A_BOLD)

    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)

    exec_cmd("crontab -l > temp")
    for key, val in attr_dict.items():
        exec_cmd("echo \"{:s} {:s} {:s}\" >> temp".format(val,
                                                          exec_file,
                                                          key))
    exec_cmd("crontab temp")
    exec_cmd("rm -f temp")

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Task was added to crontab.", NORMAL)


@screen_refresh
def remove_from_crontab():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, REM_CRONTAB_TXT, curses.A_BOLD)

    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)

    exec_cmd("crontab -l | grep -q !\"{:s}\" > temp".format(exec_file))
    exec_cmd("crontab temp")
    exec_cmd("rm -f temp")

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Task was removed from crontab.", NORMAL)


@check_confidence
@screen_refresh
def remove_backup(pos, backups):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, REMOVE_BACKUP_TXT, curses.A_BOLD)

    backup = backups[pos]

    rm_dir(os.path.join(BACKUP_DIR, backup))
    backups.remove(backup)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Remove backup: {:s}".format(backup), NORMAL)


def set_version():
    version_file_path = os.path.join(SETUP_DIR, VERSION_FILE)

    if not os.path.exists(version_file_path):
        return

    # get info from repo
    branch = exec_cmd("git rev-parse --abbrev-ref HEAD")

    if not branch:
        return

    commits = exec_cmd("git rev-list {:s} --count".format(str(branch)))
    auth = exec_cmd("git log -1 --pretty=format:\"%an\"")
    hash = exec_cmd("git log -1 --pretty=format:\"%h\"")

    # replace in version.py file values
    text_f_file = ""

    with open(version_file_path, 'r') as file:
        text_f_file = file.read()

    text_f_file = text_f_file.replace("current_commits", str(commits))
    text_f_file = text_f_file.replace("beta", str(branch))
    text_f_file = text_f_file.replace("last_commiter", str(auth))
    text_f_file = text_f_file.replace("last_hash", str(hash))

    with open(version_file_path, 'w') as file:
        file.write(text_f_file)


def install():
    create_dirs()

    copy_source()

    copy_misc()

    set_version()

    copy_config()

    change_params_context()

    add_to_crontab(UPDATE_ATTR)
    add_to_crontab(UPDATE_FULLY_ATTR)


def uninstall():
    backup_config()

    remove_dirs()

    remove_symlink()

    remove_from_crontab()


def update_files():
    copy_source()

    copy_misc()

    set_version()


def get_last_backup():
    backups = get_list_of_backups()
    return max(backups) if backups else ""


def get_list_of_backups():
    backups_list = []

    temp_list = os.listdir(BACKUP_DIR)

    for item in temp_list:
        item_path = os.path.join(BACKUP_DIR, item)
        if os.path.isdir(item_path):
            backups_list.append(item)
        else:
            rm_file(item_path)

    return backups_list


def backups_context():
    backups = sorted(get_list_of_backups())

    if backups:
        selected = backups_menu_loop(backups)

        if selected != "":
            restore_cfg(selected)


def change_params_context():
    set_default_selecting()

    if params_menu_loop():
        create_executable()
        create_symlink()
    else:
        set_default_selecting()


def try_load_params_from_executable():
    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)

    same_line_splitted = read_exec_file_same_line_splitted(exec_file)

    if same_line_splitted:
        for part in same_line_splitted:
            if len(part) == 2:
                for key in PARAMS_MENU_STATE.keys():
                    if part == PARAMS_MENU_STATE[key][2]:
                        PARAMS_MENU_STATE[key][1] = True

                        break

        return True

    return False


def reset_params():
    for key in PARAMS_MENU_STATE.keys():
        PARAMS_MENU_STATE[key][1] = False


def set_default_selecting():
    if not try_load_params_from_executable():
        reset_params()


def get_params_str():
    params_str = " ".join([PARAMS_MENU_STATE[key][2] for key in PARAMS_MENU_STATE.keys() if PARAMS_MENU_STATE[key][1]])

    return params_str


@screen_height_update
@screen_refresh
def show_backups_menu(pos, backups_list):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, BACKUPS_MENU_NAME_TXT, curses.A_BOLD)

    for backup in backups_list:
        id = backups_list.index(backup)

        if id == pos:
            SCREEN.addstr(BODY_HEIGHT + id, CUR_WIDTH + 2, backup, HIGHLIGHT)
        else:
            SCREEN.addstr(BODY_HEIGHT + id, CUR_WIDTH + 2, backup, NORMAL)

    SCREEN.addstr(BODY_HEIGHT + len(backups_list) + 2, CUR_WIDTH + 2, "ENTER - restore, DEL - remove, ESC - cancel", NORMAL)


@screen_height_update
@screen_refresh
def show_select_params_menu(pos):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, PARAMS_MENU_NAME_TXT, curses.A_BOLD)

    max = 0

    for key in PARAMS_MENU_STATE.keys():
        id = PARAMS_MENU_STATE[key][0]

        if id > max:
            max = id

        state = PARAMS_MENU_STATE[key][1]
        text = "({:s}) {:s}".format(("*" if state else " "),
                                    key)

        if pos == id:
            SCREEN.addstr(BODY_HEIGHT + id, CUR_WIDTH + 2, text, HIGHLIGHT)
        else:
            SCREEN.addstr(BODY_HEIGHT + id, CUR_WIDTH + 2, text, NORMAL)

    SCREEN.addstr(BODY_HEIGHT + max + 3, CUR_WIDTH + 2, "SPACE - select, ENTER - accept, ESC - cancel", NORMAL)


@screen_height_update
@screen_refresh
def show_main_menu(pos):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, MENU_NAME_TXT, curses.A_BOLD)

    for i in range(0, MAIN_M_SZ):
        if pos == i:
            SCREEN.addstr(BODY_HEIGHT + i, CUR_WIDTH + 2, MAIN_M[i], HIGHLIGHT)
        else:
            SCREEN.addstr(BODY_HEIGHT + i, CUR_WIDTH + 2, MAIN_M[i], NORMAL)

    SCREEN.addstr(BODY_HEIGHT + MAIN_M_SZ + 2, CUR_WIDTH + 2, "ENTER - accept, ESC - exit", NORMAL)


def true_exit(res, msg=""):
    curses.endwin()

    if res != 0:
        print("Error number {:d}. Error Message: {:s}".format(res, msg))

    exit(res)


def get_key():
    key = ""
    try:
        key = SCREEN.getch()
    except KeyboardInterrupt:
        true_exit(0)
    return key


def backups_menu_accept_actions(pos, backups_list):
    return backups_list[pos] if pos < len(backups_list) else ""


def param_menu_accept_actions(pos):
    for key in PARAMS_MENU_STATE.keys():
        if pos == PARAMS_MENU_STATE[key][0]:
            state = PARAMS_MENU_STATE[key][1]

            if state:
                state = False
            else:
                state = True

            PARAMS_MENU_STATE[key][1] = state


def main_menu_accept_action(pos):
    pos_text = MAIN_M[pos]

    if pos_text == M_INSTALL:
        install()
    elif pos_text == M_UNINSTALL:
        uninstall()
    elif pos_text == M_UPDATE_FILES:
        update_files()
    elif pos_text == M_CHANGE_PARAMS:
        change_params_context()
    elif pos_text == M_RESTORE_CFG:
        backups_context()
    elif pos_text == M_EXIT:
        true_exit(0)


def main_menu_loop():
    pos = 0

    show_main_menu(pos)

    key = get_key()

    while key != KEY_ESC:
        if key == curses.KEY_UP:
            if pos > 0:
                pos = pos - 1
            else:
                pos = MAIN_M_SZ - 1
        elif key == curses.KEY_DOWN:
            if pos < MAIN_M_SZ - 1:
                pos = pos + 1
            else:
                pos = 0
        elif key == curses.KEY_ENTER or key == KEY_RETURN:
            main_menu_accept_action(pos)

        show_main_menu(pos)
        key = get_key()


def params_menu_loop():
    pos = 0

    show_select_params_menu(pos)

    key = get_key()
    while key != KEY_ESC:
        if key == curses.KEY_UP:
            if pos > 0:
                pos = pos - 1
            else:
                pos = PARAMS_MENU_SZ - 1
        elif key == curses.KEY_DOWN:
            if pos < PARAMS_MENU_SZ - 1:
                pos = pos + 1
            else:
                pos = 0
        elif key == curses.KEY_ENTER or key == KEY_RETURN:
            return True
        elif key == KEY_SPACE:
            param_menu_accept_actions(pos)

        show_select_params_menu(pos)
        key = get_key()

    return False


def backups_menu_loop(backups_list):
    pos = 0

    res = ""

    show_backups_menu(pos, backups_list)
    menu_sz = len(backups_list)

    key = get_key()
    while key != KEY_ESC:
        if key == curses.KEY_UP:
            if pos > 0:
                pos = pos - 1
            else:
                pos = menu_sz - 1
        elif key == curses.KEY_DOWN:
            if pos < menu_sz - 1:
                pos = pos + 1
            else:
                pos = 0
        elif key == KEY_DELETE:
            remove_backup(pos, backups_list)
            menu_sz = len(backups_list)
            pos = 0
        elif key == curses.KEY_ENTER or key == KEY_RETURN:
            return backups_menu_accept_actions(pos, backups_list)

        if menu_sz <= 0:
            break

        show_backups_menu(pos, backups_list)
        key = get_key()

    return ""


def init_curses(screen):
    global HIGHLIGHT
    global NORMAL
    global SCREEN

    SCREEN = screen
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    SCREEN.keypad(1)

    curses.init_pair(1,
                     curses.COLOR_BLACK,
                     curses.COLOR_WHITE)

    HIGHLIGHT = curses.color_pair(1)
    NORMAL = curses.A_NORMAL

    SCREEN.border(0)
    curses.curs_set(0)


def main(screen):
    init_curses(screen)

    main_menu_loop()

    true_exit(0)


if __name__ == "__main__":
    curses.wrapper(main)



