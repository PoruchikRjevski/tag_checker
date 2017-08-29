#!/bin/bash

CUR_DIR="./"
SETUP_DIR="/usr/local/bin/tag_checker/"
OUT_DIR="/var/www/swver_hist/"
OUT_DEV_DIR=$OUT_DIR"devices/"
OUT_ORD_DIR=$OUT_DEV_DIR"orders/"
SRC_DIR="src/"
PY_FILES="*.py"
CONFIG_DIR="/etc/"
CONFIG_FILE="tag_checker.ini"
TRANSLATE_FILE="tag_checker_translate"
NAME="tag_checker.py"

PYTHON="python3"


# check and remove file
check_and_rem_f() {    
    if [ -f "$1" ] 
    then
        sudo rm -f $1
    fi
}

# check and remove dir
check_and_rem_d() {    
    if [ -d "$1" ] 
    then
        sudo rm -rf $1
    fi
}

# check an make dir
check_and_make_d() {
    if [ ! -d "$1" ] 
    then
        sudo mkdir -p $1
    fi
}

# ---------------------------------
# main
# ---------------------------------
main() {
    # CHECKS
    # check pyton
    if ! which $PYTHON > /dev/null; then
        echo "Please, install python3 before using $0"
        exit 0
    fi

    # ASKS
    # ask about log and update
    cmd="-q"
    
    read -p "Log (y/n)? " answ
    case "$answ" in 
      y|Y ) log=$"-l";;
      n|N ) ;;
      * ) exit 1;;
    esac
    
    read -p "Update repo's before scan (y/n)? " answ
    case "$answ" in 
      y|Y ) upd="-u";;
      n|N ) ;;
      * ) exit 1;;
    esac

    read -p "Switch branch to develop? " answ
    case "$answ" in 
      y|Y ) dev="-d";;
      n|N ) ;;
      * ) exit 1;;
    esac
    
    read -p "Exec cmd's by sudo? " answ
    case "$answ" in 
      y|Y ) sud="-s";;
      n|N ) ;;
      * ) exit 1;;
    esac
    
    # COPY
    # prepare
    check_and_make_d "$SETUP_DIR"
    check_and_make_d "$OUT_DIR"
    check_and_make_d "$OUT_ORD_DIR"
    
    # copy files
    sudo cp -rf $SRC_DIR$PY_FILES $SETUP_DIR

    #check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    sudo cp -rf $CUR_DIR$CONFIG_FILE $CONFIG_DIR
    
    #check_and_rem_f "$CONFIG_DIR$TRANSLATE_FILE"
    sudo cp -rf $CUR_DIR$TRANSLATE_FILE $CONFIG_DIR
    
    # CRON
    # del from cron old note(s)
    crontab -l | grep -q !"$NAME" > temp
    crontab temp
    rm temp
    
    # add to cron
    crontab -l > temp
    echo "1-59 * * * * $SETUP_DIR$NAME $cmd $log $upd $sud $dev" >> temp
    crontab temp
    rm temp
    
    exit 0
}

main
