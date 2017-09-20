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
ONE=1
TWO=2
THREE=3
FOUR=4
FIVE=5
SIX=6
SEV=7
EIGHT=8
NINE=9

# parameters
def_ar=("" "" "" "" "" "")
sw_on="on"
sw_off="off"

sud="-s"
mt="-m"
deb="-d"
tim="-t"
quiet="-q"
log="-l"

setted_params=("${def_ar[@]}")
setted_params_sw=("${def_ar[@]}")

# dialogs
dialog=(dialog)

wnd_sz="20 50"
wnd_sz_f="20 50 9"

main_menu_dlg=(--clear \
               --title "Tag Checker Installer" \
               --menu "Main menu" $wnd_sz_f)

change_params_dlg=(--clear \
                   --title "Change parameters" \
                   --checklist "Run parameters" $wnd_sz_f)

progress_dlg=(--clear \
              --gauge "Processing" $wnd_sz)
full_inst_title=(--title "Full install")
full_uninst_title=(--title "Full uninstall")
after_change_pararms_title=(--title "Create files")
create_dirs_title=(--title "Create dirs")

m_m_opts=(1 "Full install"
          2 "Full uninstall"
          3 "Update files"
          4 "Change parameters"
          5 "Edit crontab"
          6 "Run from source"
          7 "Run from installed"
          8 "Show menu"
          9 "Exit from installer")    

# check and remove file
check_and_rem_f() {    
    if [ -f "$1" ] 
    then
        rm -f $1 > /dev/null 2>&1 &
    fi
}

# check and remove dir
check_and_rem_d() {    
    if [ -d "$1" ] 
    then
        rm -rf $1 > /dev/null 2>&1 &
    fi
}

# check an make dir
check_and_make_d() {
    if [ ! -d "$1" ] 
    then
        mkdir -p $ > /dev/null 2>&1 &
    fi
}

# create executable file
create_exec_file() {
    touch $SETUP_DIR$EXEC_F > /dev/null 2>&1 &
    
    chmod +x $SETUP_DIR$EXEC_F > /dev/null 2>&1 &
    
    echo $PREFIX_F > $SETUP_DIR$EXEC_F
    echo $SETUP_DIR$NAME $quiet $log $sud $mt $deb $tim '$@' >> $SETUP_DIR$EXEC_F
}

# create link
create_link() {
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    ln -s $SETUP_DIR$EXEC_F $LINK_PATH$TAG_CHECKER > /dev/null 2>&1 &
}

#  build ver
build_ver() {
    branch=$($GIT rev-parse --abbrev-ref HEAD) > /dev/null 2>&1 &
    commits=$($GIT rev-list $branch --count) > /dev/null 2>&1 &
    last_author=$($GIT log -1 --pretty=format:"%an") > /dev/null 2>&1 &
    last_hash=$($GIT log -1 --pretty=format:"%h") > /dev/null 2>&1 &

    sed -Ei "s/current_commits/$commits/g" $SETUP_DIR$VERSION_FILE
    sed -i "s@beta@$branch@" $SETUP_DIR$VERSION_FILE
    sed -i "s@last_commiter@$last_author@" $SETUP_DIR$VERSION_FILE
    sed -i "s@last_hash@$last_hash@" $SETUP_DIR$VERSION_FILE
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
    clear
    choise=$("${dialog[@]}" "${main_menu_dlg[@]}" "${m_m_opts[@]}" 2>&1 >/dev/tty)
    clear
    case $choise in
        1 ) full_install;;
        2 ) full_uninstall;;
        3 ) 
            clear
            (
                progress_step "Init updating files" 0

                progress_step "Remove $SETUP_DIR" 5
                check_and_rem_d "$SETUP_DIR" > /dev/null 2>&1 &

                progress_step "make $SETUP_DIR." 15
                check_and_make_d "$SETUP_DIR" > /dev/null 2>&1 &

                progress_step "Update files" 20
            ) | $("${dialog[@]}" "${create_dirs_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

            update_files

            (
                progress_step "Finish updating files" 100
            ) | $("${dialog[@]}" "${create_dirs_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

            show_msg "Files was updated."
            clear
        ;;
        4 ) 
            change_parameters
            show_msg "Parameters accepted. Use link: $TAG_CHECKER."
            clear
            ;;
        5 ) edit_crontab;;
        6 ) run_from_source;;
        7 ) run_now;;
        8 ) show_main_menu;;
        9 ) exit 0;;
    esac

    main_menu
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
    clear
    (
        progress_step "Init updating files" 0

        progress_step "Script files was copied" 10
        yes | cp -rf $SRC_DIR* $SETUP_DIR > /dev/null 2>&1 &

        progress_step "Config file was checked." 15
        cp -rfn $CUR_DIR$CONFIG_FILE $CONFIG_DIR > /dev/null 2>&1 &
        chmod 777 $CONFIG_DIR$CONFIG_FILE > /dev/null 2>&1 &

        progress_step "Copy scripts" 20
        cp $CUR_DIR$SRC_DIR$MISC_DIR$SCRIPTS_FILE $OUT_DIR > /dev/null 2>&1 &

        progress_step "Copy styles" 25
        cp $CUR_DIR$SRC_DIR$MISC_DIR$STYLE_FILE $OUT_DIR > /dev/null 2>&1 &

        progress_step "Create build version" 50
        build_ver

        progress_step "Create exec file" 75
        create_exec_file

        progress_step "Create link" 90
        create_link

        progress_step "Finish updating files" 100
    ) | $("${dialog[@]}" "${create_dirs_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

# delete dirs
delete_dirs() {
    check_and_rem_d "$SETUP_DIR"
    check_and_rem_d "$OUT_DIR"
    check_and_rem_d "$LOG_DIR"

    echo "SETUP, OUT and LOG dirs was deleted."
}

# create dirs
create_dirs() {
    clear
    (
        progress_step "make $SETUP_DIR" 35
        check_and_make_d "$SETUP_DIR"
        chmod +x $SETUP_DIR* > /dev/null 2>&1 &

        progress_step "make $OUT_ORD_DIR" 75
        check_and_make_d "$OUT_ORD_DIR"
        chmod +x $OUT_ORD_DIR* > /dev/null 2>&1 &

        progress_step "make $LOG_DIR" 100
        check_and_make_d "$LOG_DIR"
        chmod +x $LOG_DIR* > /dev/null 2>&1 &
    ) | $("${dialog[@]}" "${create_dirs_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

# reset attributes
change_parameters() {
    changed=("${def_ar[@]}")
    changed_sw=("${def_ar[@]}")

    c_p_opts=(1 "Run cmd's as sudo." "${setted_params_sw[1]}"
              2 "Multithreading on." "${setted_params_sw[2]}"
              3 "Debug out on." "${setted_params_sw[3]}"
              4 "Timings out." "${setted_params_sw[4]}"
              5 "Out logs to stdout." "${setted_params_sw[5]}"
              6 "Logging on." "${setted_params_sw[6]}")


    choises=$("${dialog[@]}" "${change_params_dlg[@]}" "${c_p_opts[@]}" 2>&1 >/dev/tty)

    for choise in $choises
    do
        case $choise in
            1) changed[1]="$sud" changed_sw[1]="on";;
            2) changed[2]="$mt" changed_sw[2]="on";;
            3) changed[3]="$deb" changed_sw[3]="on";;
            4) changed[4]="$tim" changed_sw[4]="on";;
            5) changed[5]="$quiet" changed_sw[5]="on";;
            6) changed[6]="$log" changed_sw[6]="on";;
        esac
    done

    setted_params=("${changed[@]}")
    setted_params_sw=("${changed_sw[@]}")

    (
        progress_step "Init create addition files" 0
        progress_step "Create exec file" 50
        create_exec_file

        progress_step "Create link" 100
        create_link
    ) | $("${dialog[@]}" "${after_change_pararms_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    clear

    main_menu
}

show_msg() {
    msgbox_dlg=(--title "Message" --msgbox "$1" $wnd_sz)
    $("${dialog[@]}" "${msgbox_dlg[@]}" 2>&1 >/dev/tty)
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

progress_step() {
        echo $2
        echo "XXX"
        echo $1
        echo "XXX"
        sleep 0.5
        pct=$2 
}

# full install
full_install() {
    (
        progress_step "Init installing" 5
        
        progress_step "Create dirs\n" 35
    ) | $("${dialog[@]}" "${full_inst_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    create_dirs
    
    (
        progress_step "Update files" 65
    ) | $("${dialog[@]}" "${full_inst_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    update_files

    (
        progress_step "Change parameters" 80
    ) | $("${dialog[@]}" "${full_inst_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    change_parameters

    (
        progress_step "Edit crontab" 90
    ) | $("${dialog[@]}" "${full_inst_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)

    edit_crontab

    (
        progress_step "Finish installing" 100
    ) | $("${dialog[@]}" "${full_inst_title[@]}" "${progress_dlg[@]}" 2>&1 >/dev/tty)
    
    clear

    show_msg "Parameters accepted. Use link: $TAG_CHECKER."

    clear

    main_menu
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

    
    # choise=$(dialog --clear \
    #                  --backtitle "Backtitle" \
    #                  --menu "Menu" 40 50 10 \
    #                  "${m_m_opts[@]}" \
    #                  2>&1 >/dev/tty)

    # clear
    # case $CHOICE in
    #     1)
    #         echo "You chose Option 1"
    #         ;;
    #     2)
    #         echo "You chose Option 2"
    #         ;;
    #     3)
    #         echo "You chose Option 3"
    #         ;;
    # esac


# COUNT=10
# (
# while test $COUNT != 110
# do
# echo $COUNT
# echo "XXX"
# echo "Новое сообщение ($COUNT процентов)"
# echo "Строка 2"
# echo "XXX"
# COUNT=`expr $COUNT + 10`
# sleep 1
# done
# ) |
# $DIALOG --title "Индикатор" --gauge "А вот пример простейшего индикатора" 20 70 0

    exit 0
}

main
