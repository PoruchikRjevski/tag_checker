#!/usr/bin/sudo python3

import os
import sys
import shutil
import time

import curses

# INSTALLER DEFS
SOLUTION_NAME = "tag_checker"
OUT_LOG_DIR= "/tmp/{:s}_log/".format(SOLUTION_NAME)
SETUP_DIR = "/opt/{:s}/".format(SOLUTION_NAME)
OUT_DIR = "/var/www/swver_hist/"
OUT_DEV_DIR = "{:s}devices/".format(OUT_DIR)
OUT_ORD_DIR = "{:s}orders/".format(OUT_DEV_DIR)
CSS_DIR = "css/"
JS_DIR = "js/"
OUT_JS_DIR = "{:s}{:s}".format(OUT_DIR, JS_DIR)
OUT_CSS_DIR = "{:s}{:s}".format(OUT_DIR, CSS_DIR)
SRC_DIR="src/"

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
HEAD_TXT_SZ = len(HEAD_TXT) // 2

HEAD_HEIGHT = 2
NAME_HEIGHT = 4
BODY_HEIGHT = 6
CUR_WIDTH = 0


KEY_RETURN = 10


def screen_refresh(func):
    def wrapped(pos, *args, **kwargs):
        global CUR_WIDTH
        _, width = SCREEN.getmaxyx()

        CUR_WIDTH = (width // 2) - HEAD_TXT_SZ

        SCREEN.clear()
        SCREEN.border(0)

        SCREEN.addstr(HEAD_HEIGHT, CUR_WIDTH + 2, HEAD_TXT, curses.A_STANDOUT | curses.A_BOLD)

        func(pos)

        SCREEN.refresh()
    return wrapped

@screen_refresh
def create_dir(path):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, CREATING_DIRS_TXT, curses.A_BOLD)

    if not os.path.exists(path):
        os.makedirs(path)
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Create dir: {:s}".format(path), NORMAL)
    else:
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Dir already exist: {:s}".format(path), NORMAL)

    time.sleep(0.1)


@screen_refresh
def remove_dir(path):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, REMOVING_DIRS_TXT, curses.A_BOLD)

    if os.path.exists(path):
        shutil.rmtree(path)
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Remove dir: {:s}".format(path), NORMAL)
    else:
        SCREEN.addstr(BODY_HEIGHT, CUR_WIDTH + 2, "Dir already removed: {:s}".format(path), NORMAL)

    time.sleep(0.1)


def create_dirs():
    create_dir(SETUP_DIR)
    create_dir(OUT_ORD_DIR)
    create_dir(OUT_CSS_DIR)
    create_dir(OUT_JS_DIR)
    create_dir(OUT_LOG_DIR)


def remove_dirs():
    remove_dir(SETUP_DIR)
    remove_dir(OUT_ORD_DIR)
    remove_dir(OUT_CSS_DIR)
    remove_dir(OUT_JS_DIR)
    remove_dir(OUT_LOG_DIR)


def install():
    create_dirs()
    # update files
    # change parameters
    # add crontab
    pass


def uninstall():
    remove_dirs()
    # backup and remove config files
    # remove link
    # remove crontab
    pass


def update_files():
    pass


def change_params():
    pass


@screen_refresh
def show_menu(pos):
    SCREEN.addstr(NAME_HEIGHT, CUR_WIDTH + 2, MENU_NAME_TXT, curses.A_BOLD)

    for i in range(0, MAIN_M_SZ):
        if pos == i:
            SCREEN.addstr(BODY_HEIGHT + i, CUR_WIDTH + 2, MAIN_M[i], HIGHLIGHT)
        else:
            SCREEN.addstr(BODY_HEIGHT + i, CUR_WIDTH + 2, MAIN_M[i], NORMAL)


def true_exit():
    curses.endwin()
    exit(0)


def get_key():
    key = ""
    try:
        key = SCREEN.getch()
    except KeyboardInterrupt:
        true_exit()
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
        true_exit()


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

    true_exit()

if __name__ == "__main__":
    main()



