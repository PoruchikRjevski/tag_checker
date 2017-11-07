#!/usr/bin/sudo python3

import os
import sys
import time
import subprocess
import datetime
import curses

# INSTALLER DEFS
SOLUTION_NAME = "tag_checker"
OUT_LOG_DIR= "/tmp/{:s}_log/".format(SOLUTION_NAME)
SETUP_DIR = "/opt/{:s}/".format(SOLUTION_NAME)
OUT_DIR = "/var/www/swver_hist/"
OUT_DEV_DIR = "{:s}devices/".format(OUT_DIR)
OUT_ORD_DIR = "{:s}orders/".format(OUT_DEV_DIR)
BACKUP_DIR = "/tmp/{:s}_backups/".format(SOLUTION_NAME)
CSS_DIR = "css/"
JS_DIR = "js/"
OUT_JS_DIR = "{:s}{:s}".format(OUT_DIR, JS_DIR)
OUT_CSS_DIR = "{:s}{:s}".format(OUT_DIR, CSS_DIR)
SRC_DIR = os.path.join(os.getcwd(), "src/")
CONFIG_NAME = "config"
CONFIG_EXT = ".ini"
CONFIG_DIR = "/etc/{:s}/".format(SOLUTION_NAME)
CONFIG_FILE = "{:s}{:s}".format(CONFIG_NAME,
                                CONFIG_EXT)
CONFIG_EXMPL_DIR = "config.example/"
LINK_PATH = "/usr/local/bin/"

MAIN_FILE = "main.py"

EXEC_FILE = "run.sh"

UPDATE_ATTR = "--update"

# INSTALLER VARS
SELECTED_PARAMS = []



# CURSES MENU
HIGHLIGHT = None
NORMAL = None

SCREEN = None

M_INSTALL = "Install"
M_UNINSTALL = "Uninstall"
M_UPDATE_FILES = "Update Files"
M_CHANGE_PARAMS = "Change run parameters"
M_EXIT = "Exit"

MAIN_M = [M_INSTALL, M_UNINSTALL, M_UPDATE_FILES, M_CHANGE_PARAMS, M_EXIT]
MAIN_M_SZ = len(MAIN_M)


HEAD_TXT = "Tag checker installer"
MENU_NAME_TXT = "Menu"
CREATING_DIRS_TXT = "Creating dirs"
REMOVING_DIRS_TXT = "Removing dirs"
COPYING_TXT = "Copying"
REMOVING_TXT = "Removing"
CREATE_EXEC_TXT = "Create executable"
CREATE_LN_TXT = "Create symlink"
REMOVE_LN_TXT = "Remove symlink"

HEAD_TXT_SZ = len(HEAD_TXT) // 2

HEAD_HEIGHT = 2
NAME_HEIGHT = 4
BODY_HEIGHT = 6
SCROLLBAR_HEIGHT = 10
CUR_WIDTH = 0

PROGRESS_BAR = None


KEY_RETURN = 10


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

        time.sleep(0.05)

        SCREEN.refresh()
    return wrapped


def check_existence_strong(func):
    def wrapped(arg, *argv):
        if not os.path.exists(arg):
            true_exit(1, "{:s} not exist".format(arg))

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
                            shell=True)
    proc.communicate()


@check_existence_weak
def cp_dir(src, dst):
    exec_cmd("yes | cp -rf {:s}* {:s}".format(src, dst))


@check_existence_weak
def cp_file(src, dst=""):
    exec_cmd("cp -rfn {:s} {:s}".format(src, dst))


@check_existence_weak
def rm_dir(dst):
    exec_cmd("rm -rf {:s}".format(dst))


@check_existence_weak
def rm_file(dst):
    exec_cmd("rm -f {:s}".format(dst))


@check_existence_strong
def add_runnable_rights(dst):
    exec_cmd("chmod +x {:s}".format(dst))


@check_existence_strong
def create_ln(src, dst):
    exec_cmd("ln -s {:s} {:s}".format(src, dst))


@screen_refresh
def copy_source():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)
    cp_dir(SRC_DIR, SETUP_DIR)
    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Copy: {:s} to {:s}".format(SRC_DIR, SETUP_DIR), NORMAL)


@screen_refresh
def backup_config():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)
    backup_dir = os.path.join(BACKUP_DIR,
                              "{:s}_{:s}".format(SOLUTION_NAME,
                                                 datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

    cp_dir(CONFIG_DIR, backup_dir)
    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Backup config: {:s}".format(CONFIG_FILE), NORMAL)


@screen_refresh
def copy_config():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, COPYING_TXT, curses.A_BOLD)
    src_conf_dir = os.path.join(os.getcwd(),
                                CONFIG_EXMPL_DIR)

    cp_dir(src_conf_dir, CONFIG_DIR)
    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Copied: {:s} to {:s}".format(SRC_DIR, SETUP_DIR), NORMAL)


@screen_refresh
def create_executable():
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, CREATE_EXEC_TXT, curses.A_BOLD)

    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)
    main_file = os.path.join(SETUP_DIR,
                             MAIN_FILE)

    with open(exec_file, 'w') as file:
        file.write('#!/bin/bash\n')
        file.write("{:s} {:s} $@".format(main_file,
                                         " ".join(SELECTED_PARAMS)))

    add_runnable_rights(exec_file)

    SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Created executable: {:s}".format(exec_file), NORMAL)


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
def add_to_crontab(attr):
    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)

    exec_cmd("crontab -l > temp")
    exec_cmd("echo \"0 * * * * {:s} {:s}\" >> temp".format(exec_file,
                                                                    attr))
    exec_cmd("crontab temp")
    exec_cmd("rm -f temp")


@screen_refresh
def remove_from_crontab():
    exec_file = os.path.join(SETUP_DIR,
                             EXEC_FILE)

    exec_cmd("crontab -l | grep -q !\"{:s}\" > temp".format(exec_file))
    exec_cmd("crontab temp")
    exec_cmd("rm -f temp")


def install():
    create_dirs()

    copy_source()

    copy_config()

    # select run parameters

    create_executable()
    create_symlink()

    add_to_crontab(UPDATE_ATTR)


def uninstall():
    backup_config()

    remove_dirs()

    remove_symlink()

    remove_from_crontab()


def update_files():
    pass


def change_params():
    pass


@screen_height_update
@screen_refresh
def show_menu(pos):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, MENU_NAME_TXT, curses.A_BOLD)

    for i in range(0, MAIN_M_SZ):
        if pos == i:
            SCREEN.addstr(BODY_HEIGHT + i, CUR_WIDTH + 2, MAIN_M[i], HIGHLIGHT)
        else:
            SCREEN.addstr(BODY_HEIGHT + i, CUR_WIDTH + 2, MAIN_M[i], NORMAL)


def true_exit(res, str=""):
    curses.endwin()

    if res != 0:
        print("Error number {:d}. Error Message: {:s}".format(res, str))

    exit(res)


def get_key():
    key = ""
    try:
        key = SCREEN.getch()
    except KeyboardInterrupt:
        true_exit(0)
    return key


def accept_action(pos):
    pos_text = MAIN_M[pos]

    if pos_text == M_INSTALL:
        install()
    elif pos_text == M_UNINSTALL:
        uninstall()
    elif pos_text == M_UPDATE_FILES:
        update_files()
    elif pos_text == M_CHANGE_PARAMS:
        change_params()
    elif pos_text == M_EXIT:
        true_exit(0)


def main():
    global HIGHLIGHT
    global NORMAL
    global SCREEN

    SCREEN = curses.initscr()
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

    pos = 0

    show_menu(pos)

    key = get_key()
    while key != 27:
        if key == curses.KEY_UP:
            if pos > 0:
                pos = pos - 1
        elif key == curses.KEY_DOWN:
            if pos < MAIN_M_SZ - 1:
                pos = pos + 1
        elif key == curses.KEY_ENTER or key == KEY_RETURN:
            accept_action(pos)

        show_menu(pos)
        key = get_key()

    true_exit(0)

if __name__ == "__main__":
    main()



