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
NAME="main.py"
SCRIPTS_FILE="scripts.js"
STYLE_FILE="style.css"
VERSION_FILE="version.py"
MISC_DIR="misc/"

EXEC_F="run.sh"
PREFIX_F="#!/bin/bash"

PYTHON="python3"
GIT="git"




# ----------
ONE="1"
TWO="2"
THREE="3"
FOUR="4"
FIVE="5"


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

# create executable file
create_exec_file() {
    touch $SETUP_DIR$EXEC_F
    
    chmod 777 $SETUP_DIR$EXEC_F
    
    echo $PREFIX_F > $SETUP_DIR$EXEC_F
    echo $SETUP_DIR$NAME $quiet $log $sud $mt $deb $tim >> $SETUP_DIR$EXEC_F
}

# run script
run_now() {
    $SETUP_DIR$NAME $log $sud $mt $deb $tim
}

#  build ver
build_ver() {
    commits=$($GIT rev-list --all --count)
    sed -Ei "s/current_commits/$commits/g" $SETUP_DIR$VERSION_FILE
}


# check soft installed
check_soft() {
    # check pyton
    if ! which $PYTHON > /dev/null; then
        echo "Please, install python3 before using $0"
        exit 0
    fi

    # check git
    if ! which $GIT > /dev/null; then
        echo "Please, install git before using $0"
        exit 0
    fi
}

# main menu
main_menu() {
    echo "Select action"
    echo "------"
    echo ""
    echo "[$ONE] Full install"
    echo "[$TWO] Update files"
    echo "[3] Edit crontab"
    echo "[4] Reset attributes"
    echo "[5] Run from source"
    echo ""

    read action

    case "$action" in
      $TWO ) edit_crontab;;
      * ) echo "Bad select";;
    esac
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

# edit crontab
edit_crontab() {
    echo "Edit crontab"
    echo ""
    echo "[$ONE] Add to crontab"
    echo "[$TWO] Remove from crontab"
    echo "[$THREE] Back to main"
    echo ""

    read action

    case "$action" in
      $ONE ) 
        remove_from_crontab
        add_to_crontab 
      ;;
      $TWO ) 
        remove_from_crontab
      ;;
      $THREE )
        main_menu
      ;;
      * ) echo "Bad select";;
    esac
}


# ---------------------------------
# main
# ---------------------------------
main() {
    check_soft

    main_menu

    exit 0

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
      y|Y ) mt="-m"
      ;;
      n|N ) ;;
      * ) mt="";;
    esac

    read -p "Run debug out (y/n)? " answ
    case "$answ" in 
      y|Y ) deb="-d"
      ;;
      n|N ) 
        read -p "Run timings out (y/n)? " answ
        case "$answ" in 
          y|Y ) tim="-t"
          ;;
          n|N ) ;;
          * ) tim="";;
        esac
      ;;
      * ) deb="";;
    esac
    
    # COPY
    # prepare
    check_and_rem_d "$SETUP_DIR"
    check_and_make_d "$SETUP_DIR"
    check_and_rem_d "$OUT_DIR"
    check_and_make_d "$OUT_ORD_DIR"
    
    echo "Dirs was checked."
    
    # copy files
    yes | cp -rf $SRC_DIR* $SETUP_DIR
    chmod +x $SETUP_DIR*
    
    echo "Executable files was copied."

    #check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    cp -rfn $CUR_DIR$CONFIG_FILE $CONFIG_DIR
    chmod 777 $CONFIG_DIR$CONFIG_FILE
    
    #check_and_rem_f "$CONFIG_DIR$TRANSLATE_FILE"
    cp -rfn $CUR_DIR$TRANSLATE_FILE $CONFIG_DIR
    chmod 777 $CONFIG_DIR$TRANSLATE_FILE

    check_and_rem_f "$OUT_DIR$SCRIPTS_FILE"
    cp $CUR_DIR$SRC_DIR$MISC_DIR$SCRIPTS_FILE $OUT_DIR
    check_and_rem_f "$OUT_DIR$STYLE_FILE"
    cp $CUR_DIR$SRC_DIR$MISC_DIR$STYLE_FILE $OUT_DIR
    
    create_exec_file

    # fix build ver
    build_ver

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

}

main
