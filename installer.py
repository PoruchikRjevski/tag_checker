#!/usr/bin/sudo python3

import os
import sys
from optparse import OptionParser

import curses


HIGHLIGHT = None
NORMAL = None

SCREEN = None
WIN = None

M_INSTALL = "install"
M_EXIT = "exit"

MENU = [M_INSTALL, M_EXIT]
MENU_SZ = len(MENU)

def set_options(parser):
    usage = "usage: %prog [options] [args]"

    parser.set_usage(usage)

    parser.add_option("-u", "--update",
                      action="store_true",
                      dest="update",
                      default=False,
                      help="update all")

    parser.add_option("-s", "--show",
                      action="store_true",
                      dest="show",
                      default=False,
                      help="show config, uses with '--dep [dep_name]' or alone")

def show_menu(pos):
    SCREEN.clear()
    for i in range(0, MENU_SZ):
        if pos == i:
            SCREEN.addstr(i, i, MENU[i], HIGHLIGHT)
        else:
            SCREEN.addstr(i, i, MENU[i], NORMAL)

    # SCREEN.addstr(0, 1, M_INSTALL, NORMAL)
    # SCREEN.addstr(1, 2, M_EXIT, NORMAL)
    SCREEN.refresh()

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
                     curses.COLOR_CYAN)

    HIGHLIGHT = curses.color_pair(1)
    NORMAL = curses.A_NORMAL

    SCREEN.border(0)
    curses.curs_set(0)

    pos = 0

    # win.nodelay(True)
    # win.clear()
    # win.border(1)
    # win.addstr("Menu, bitch:")
    # win.addstr("\033[1m 1st point \033[0m")
    # win.addstr("2st point")

    show_menu(pos)

    key = get_key()
    while key != 27:
        if key == curses.KEY_UP:
            if pos > 0:
                pos = pos - 1
        elif key == curses.KEY_DOWN:
            if pos < MENU_SZ - 1:
                pos = pos + 1

        show_menu(pos)
        key = get_key()

    true_exit()


    # optParser = OptionParser()
    # set_options(optParser)
    #
    # (opts, args) = optParser.parse_args()
    #
    # print("\033[1m bold suka \033[0m")
    # print("normal suka")

    # full install
    # full uninstall
    # backup config
    # change options
    # exit


if __name__ == "__main__":
    main()
    # curses.wrapper(main)



