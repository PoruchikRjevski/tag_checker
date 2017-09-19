#!/bin/bash

CUR_DIR="./"
LOG_DIR="/tmp/tag_checker_log/"
LINK_PATH="/usr/local/bin/"
SETUP_DIR="/opt/tag_checker/"
OUT_DIR="/var/www/swver_hist/"
OUT_DEV_DIR=$OUT_DIR"devices/"
OUT_ORD_DIR=$OUT_DEV_DIR"orders/"
SRC_DIR="src/"
PY_FILES="*.py"
CONFIG_DIR="/etc/"
CONFIG_FILE="tag_checker.ini"
NAME="main.py"
SCRIPTS_FILE="scripts.js"
STYLE_FILE="style.css"
VERSION_FILE="version.py"
MISC_DIR="misc/"
UPDATE_A="--update"
TAG_CHECKER="tag_checker"

EXEC_F="run.sh"
EXEC_CT_F="run_ct.sh"
PREFIX_F="#!/bin/bash"

PYTHON="python3"
GIT="git"

# cases
ONE="1"
TWO="2"
THREE="3"
FOUR="4"
FIVE="5"
SIX="6"
MENU="m"
EXIT="q"

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
    
    chmod +x $SETUP_DIR$EXEC_F
    
    echo $PREFIX_F > $SETUP_DIR$EXEC_F
    echo $SETUP_DIR$NAME $quiet $log $sud $mt $deb $tim '$@' >> $SETUP_DIR$EXEC_F

    echo "Exec file was created."
}

# create link
create_link() {
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    ln -s $SETUP_DIR$EXEC_F $LINK_PATH$TAG_CHECKER

    echo "Link was created."
}

#  build ver
build_ver() {
    branch=$($GIT rev-parse --abbrev-ref HEAD) 
    commits=$($GIT rev-list $branch --count)
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

# show main menu
show_main_menu() {
    echo ""
    echo "----------------------------"
    echo "----------------------------"
    echo "Tag Checker installer"
    echo "----------------------------"
    echo "Parameters"
    echo "----------------------------"
    echo "Out path: $OUT_DIR"
    echo "Setup path: $SETUP_DIR"
    echo "attributes: "
    if ! [ -z "$sud" ]; then
      echo "        $sud" 
    fi
    if ! [ -z "$mt" ]; then
      echo "        $mt" 
    fi
    if ! [ -z "$deb" ]; then
      echo "        $deb" 
    fi
    if ! [ -z "$tim" ]; then
      echo "        $tim" 
    fi
    if ! [ -z "$quiet" ]; then
      echo "        $quiet" 
    fi
    if ! [ -z "$log" ]; then
      echo "        $log" 
    fi
    echo "----------------------------"
    echo "Select action"
    echo "----------------------------"
    echo ""
    echo "[$ONE] Full install"
    echo "[$TWO] Full unninstall" 
    echo "[$THREE] Update files"
    echo "[$FOUR] Change parameters"
    echo "[$FIVE] Edit crontab"
    echo "[$SIX] Run from source"
    echo "[$MENU] Show menu"
    echo "[$EXIT] Exit from installer" 
    echo ""
}

# main menu
main_menu() {
    show_main_menu
    ask_menu_point

    echo ""
    echo "Succesfully out from matrix"
    echo ""
    echo "----------------------------"
    echo ""
}

ask_menu_point() {
    echo ""
    read -p "Red or blue, Neo:" action

    case "$action" in
      $ONE ) full_install;;
      $TWO ) full_uninstall;;
      $THREE ) update_files;;
      $FOUR ) change_parameters;;
      $FIVE ) edit_crontab;;
      $SIX ) run_from_source;;
      $MENU ) show_main_menu;;
      $EXIT ) exit 0;;
      * ) echo "Bad select";;
    esac

    ask_menu_point
}

# remove note from crontab
remove_from_crontab() {
    crontab -l | grep -q !"$NAME" > temp
    crontab temp
    rm temp

    echo "Crontab was cleared."
}

# add note to crontab
add_to_crontab() {
    crontab -l > temp
    echo "0 * * * * $SETUP_DIR$EXEC_F --update" >> temp
    crontab temp
    rm temp

    echo "Note was added to crontab."
}

# edit crontab
edit_crontab() {
    echo ""
    echo "--------------"
    echo "Edit crontab"
    echo "--------------"
    echo ""
    echo "[$ONE] Add to crontab"
    echo "[$TWO] Remove from crontab"
    echo "[$THREE] Cancel"
    echo ""

    read action

    case "$action" in
      $ONE ) 
        remove_from_crontab
        add_to_crontab 
      ;;
      $TWO ) remove_from_crontab;;
      $THREE );;
      * ) echo "Bad select";;
    esac
}

# update files
update_files() {
    echo ""
    echo "--------------"
    echo "Updating files."
    echo "--------------"

    delete_dirs

    # prepare
    check_and_make_d "$SETUP_DIR"
    check_and_make_d "$OUT_ORD_DIR"
    
    echo "Dirs was checked."
    
    # copy files
    yes | cp -rf $SRC_DIR* $SETUP_DIR
    chmod +x $SETUP_DIR*
    
    echo "Script files was copied."

    #check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    cp -rfn $CUR_DIR$CONFIG_FILE $CONFIG_DIR
    chmod 777 $CONFIG_DIR$CONFIG_FILE

    echo "Config file was checked."

    #check_and_rem_f "$OUT_DIR$SCRIPTS_FILE"
    cp $CUR_DIR$SRC_DIR$MISC_DIR$SCRIPTS_FILE $OUT_DIR
    #check_and_rem_f "$OUT_DIR$STYLE_FILE"
    cp $CUR_DIR$SRC_DIR$MISC_DIR$STYLE_FILE $OUT_DIR

    build_ver

    echo "Files was fully updated."
    echo ""
}

# delete files
delete_dirs() {
    check_and_rem_d "$SETUP_DIR"
    check_and_rem_d "$OUT_DIR"
    check_and_rem_d "$LOG_DIR"

    echo "Setup, out and log dirs was deleted."
}

# reset attributes
change_parameters() {
    echo ""
    echo "--------------"
    echo "Changing parameters."
    echo "--------------"

    read -p "Exec all shell commands by sudo (y/n)? " answ
    case "$answ" in 
      y|Y ) sud="-s";;
      n|N ) ;;
      * ) sud="-s";;
    esac
    
    read -p "Run with multithreading (y/n)? " answ
    case "$answ" in 
      y|Y ) mt="-m";;
      n|N ) ;;
      * ) mt="-m";;
    esac

    read -p "Switch on debug out (y/n)? " answ
    case "$answ" in 
      y|Y ) deb="-d";;
      n|N ) ;;
      * ) deb="-d";;
    esac

    if [ -z "$deb" ]; then
      read -p "Run timings out (y/n)? " answ
      case "$answ" in 
        y|Y ) tim="-t";;
        n|N ) ;;
        * ) tim="-t";;
      esac
    fi

    if ! [ -z "$tim" ] || ! [ -z "$deb" ]; then
      read -p "Move logs to stdout (y/n)? " answ
      case "$answ" in 
        y|Y );;
        n|N ) quiet="-q";;
      * ) quiet="";;
      esac
        
      read -p "Move logs to file (y/n)? " answ
      case "$answ" in 
        y|Y ) log="-l";;
        n|N ) ;;
      * ) log="-l";;
      esac
    fi

    echo "New parameters was accepted."

    create_exec_file
    create_link
}

# run_from_source
run_from_source() {
    echo ""
    echo "--------------"
    echo "Running from source."
    echo "--------------"

    change_parameters

    $CUR_DIR$SRC_DIR$NAME $quiet $log $sud $mt $deb $tim $UPDATE_A

    echo "Script from source was run."
}

# full install
full_install() {
    echo ""
    echo "--------------"
    echo "Full installing."
    echo "--------------"

    update_files
    change_parameters
    edit_crontab

    echo ""
    read -p "Run installed script now (y/n)? " answ
    case "$answ" in 
      y|Y ) run_now;;
      n|N );;
      * ) ;;
    esac
}

# full uninstall
full_uninstall() {
    echo ""
    echo "--------------"
    echo "Full uninstalling."
    echo "--------------"

    delete_dirs

    check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    echo "Config file and link was deleted."

    remove_from_crontab
}

# run installed now
run_now() {
    echo ""
    echo "--------------"
    echo "Running installed script."
    echo "--------------"

    $TAG_CHECKER $UPDATE_A

    echo "Installed script was run."
}

# ---------------------------------
# main
# ---------------------------------
main() {
    check_soft

    main_menu

    exit 0
}

main
