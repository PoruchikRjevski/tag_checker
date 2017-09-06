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
SCRIPTS_FILE="scripts.js"
STYLE_FILE="style.css"

EXEC_F="run.sh"
PREFIX_F="#!/bin/bash"

PYTHON="python3"


# check and remove file
check_and_rem_f() {    
    if [ -f "$1" ] 
    then
        rm -f $1
    fi
}

# check and remove dir
check_and_rem_d() {    
    if [ -d "$1" ] 
    then
        rm -rf $1
    fi
}

# check an make dir
check_and_make_d() {
    if [ ! -d "$1" ] 
    then
        mkdir -p $1
    fi
}

# remove note from crontab
remove_from_crontab() {
    crontab -l | grep -q !"$NAME" > temp
    crontab temp
    rm temp
}

# add note to crontab
add_to_crontab() {
    crontab -l > temp
    echo "0 * * * * $SETUP_DIR$EXEC_F" >> temp
    crontab temp
    rm temp
}

# create executable file
create_exec_file() {
    touch $SETUP_DIR$EXEC_F
    
    chmod 777 $SETUP_DIR$EXEC_F
    
    echo $PREFIX_F > $SETUP_DIR$EXEC_F
    echo $SETUP_DIR$NAME $quiet $log $upd $sud $dev $mt $fcm >> $SETUP_DIR$EXEC_F
}

# run script
run_now() {
    $SETUP_DIR$NAME $log $upd $sud $dev $mt $fcm
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
    quiet="-q"
    
    read -p "Log (y/n)? " answ
    case "$answ" in 
      y|Y ) log="-l";;
      n|N ) ;;
      * ) log="";;
    esac
    
    read -p "Exec cmd's by sudo (y/n)? " answ
    case "$answ" in 
      y|Y ) sud="-s";;
      n|N ) ;;
      * ) sud="";;
    esac
    
    read -p "Run multithreading (y/n)? " answ
    case "$answ" in 
      y|Y ) 
      mt="-m"
      
      read -p "Run multithreading fetch to cpu' cores (y/n)? " answ
      case "$answ" in 
        y|Y ) fcm="-f";;
        n|N ) ;;
        * ) fcm="";;
      esac
      ;;
      n|N ) ;;
      * ) mt="";;
    esac
    
    read -p "Update repo's before scan (y/n)? " answ
    case "$answ" in 
      y|Y ) upd="-u";;
      n|N ) ;;
      * ) upd="";;
    esac

    read -p "Switch branch to develop (y/n)? " answ
    case "$answ" in 
      y|Y ) dev="-d";;
      n|N ) ;;
      * ) dev="";;
    esac
    
    # COPY
    # prepare
    check_and_make_d "$SETUP_DIR"
    check_and_make_d "$OUT_DIR"
    check_and_make_d "$OUT_ORD_DIR"
    
    echo "Dirs was checked."
    
    # copy files
    yes | cp -rf $SRC_DIR$PY_FILES $SETUP_DIR
    chmod +x $SETUP_DIR*
    
    echo "Executable files was copied."

    #check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    cp -rfn $CUR_DIR$CONFIG_FILE $CONFIG_DIR
    chmod 777 $CONFIG_DIR$CONFIG_FILE
    
    #check_and_rem_f "$CONFIG_DIR$TRANSLATE_FILE"
    cp -rfn $CUR_DIR$TRANSLATE_FILE $CONFIG_DIR
    chmod 777 $CONFIG_DIR$TRANSLATE_FILE

    check_and_rem_f "$OUT_DIR$SCRIPTS_FILE"
    cp $CUR_DIR$SRC_DIR$SCRIPTS_FILE $OUT_DIR
    check_and_rem_f "$OUT_DIR$STYLE_FILE"
    cp $CUR_DIR$SRC_DIR$STYLE_FILE $OUT_DIR
    
    create_exec_file
    
    # CRON
    read -p "Add to crontab (y/n)? " answ
    case "$answ" in 
      y|Y ) 
      remove_from_crontab
      add_to_crontab      
      ;;
      n|N )
      remove_from_crontab
      ;;
      * ) ;;
    esac
    
    # CRON
    read -p "Run now (y/n)? " answ
    case "$answ" in 
      y|Y ) 
      run_now   
      ;;
      n|N )
      ;;
      * ) ;;
    esac
    
    exit 0
}

main
