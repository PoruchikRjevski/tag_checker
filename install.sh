#!/bin/bash

CUR_DIR="./"
SETUP_DIR="/usr/local/bin/tag_checker/"
SRC_DIR="src/"
PY_FILES="*.py"
CONFIG_DIR="/etc/"
CONFIG_FILE="tag_checker.ini"
NAME="tag_checker.py"

PYTHON="python3"

# ---------------------------------
# main
# ---------------------------------
main() {
    # check pyton
    if ! which $PYTHON > /dev/null; then
        echo "Please, install python3 before using $0"
        exit 0
    fi

    # ask about log and update
    cmd="-q"
    
    read -p "Log (y/n)? " answ
    case "$answ" in 
      y|Y ) log=$"-l";;
      n|N ) ;;
      * ) exit 1;;
    esac
    
    read -p "Update repo before scan (y/n)? " answ
    case "$answ" in 
      y|Y ) upd="-u";;
      n|N ) ;;
      * ) exit 1;;
    esac
    
    # copy script
    if [ -d "$SETUP_DIR" ] 
    then
        sudo rm -rf $SETUP_DIR
    fi
    
    sudo mkdir $SETUP_DIR
    
    sudo cp -rf $SRC_DIR$PY_FILES $SETUP_DIR

    if [ -f "$CONFIG_DIR$CONFIG_FILE" ] 
    then
        sudo rm -f $CONFIG_DIR$CONFIG_FILE
    fi
    sudo cp -rf $CUR_DIR$CONFIG_FILE $CONFIG_DIR
    
    # del from cron old note
    crontab -l | grep -q !"$NAME" > temp
    crontab temp
    rm temp
    
    # add to cron
    crontab -l > temp
    echo "1-59 * * * * $SETUP_DIR$NAME $cmd $log $upd" >> temp
    crontab temp
    rm temp
    
    
    exit 0
}


main
