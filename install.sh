#!/bin/bash

CUR_DIR="./"
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
PREFIX_F="#!/bin/bash"

PYTHON="python3"
GIT="git"

# cases
ONE="1"
TWO="2"
THREE="3"
FOUR="4"
FIVE="5"
EXIT="q"

# attributes
sud=""
mt=""
deb=""
tim=""
quiet=""
log=""

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
    echo "[$TWO] Update files"
    echo "[$THREE] Edit crontab"
    echo "[$FOUR] Reset attributes"
    echo "[$FIVE] Run from source"
    echo "[$EXIT] Exit from installer" 
    echo ""

    read action

    case "$action" in
      $ONE ) full_install;;
      $TWO ) update_files;;
      $THREE ) edit_crontab;;
      $FOUR ) change_attributes;;
      $FIVE ) run_from_source;;
      $EXIT ) exit 0;;
      * ) echo "Bad select";;
    esac

    main_menu

    echo ""
    echo "----------------------------"
    echo ""
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
    echo "0 * * * * $TAG_CHECKER $UPDATE_A" >> temp
    crontab temp
    rm temp
}

# edit crontab
edit_crontab() {
    echo "Edit crontab"
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
    # prepare
    check_and_rem_d "$SETUP_DIR"
    check_and_make_d "$SETUP_DIR"
    check_and_rem_d "$OUT_DIR"
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

    check_and_rem_f "$OUT_DIR$SCRIPTS_FILE"
    cp $CUR_DIR$SRC_DIR$MISC_DIR$SCRIPTS_FILE $OUT_DIR
    check_and_rem_f "$OUT_DIR$STYLE_FILE"
    cp $CUR_DIR$SRC_DIR$MISC_DIR$STYLE_FILE $OUT_DIR

    build_ver

    echo "Files was fully updated."
    echo ""
}

# reset attributes
change_attributes() {
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

    create_exec_file
    create_link
}

# run_from_source
run_from_source() {
    change_attributes

    $CUR_DIR$SRC_DIR$NAME $quiet $log $sud $mt $deb $tim $UPDATE_A
}

# full install
full_install() {
    update_files
    change_attributes
    edit_crontab
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
