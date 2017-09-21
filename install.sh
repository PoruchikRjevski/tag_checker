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

wnd_sz="8 78"
wnd_sz_f="20 78 10"
wnd_sz_g="20 78 0"

change_params_dlg=(--clear \
                   --title "Change parameters" \
                   --checklist "Run parameters" $wnd_sz_f)

full_inst_title=(--title "Full install")
full_uninst_title=(--title "Full uninstall")
after_change_pararms_title=(--title "Create files")
create_dirs_title=(--title "Create dirs")

# check and remove file
check_and_rem_f() {    
    if [ -f "$1" ] 
    then
        rm -f $1 &> /dev/null
    fi
}

# check and remove dir
check_and_rem_d() {    
    if [ -d "$1" ] 
    then
        rm -rf $1 &> /dev/null
    fi
}

# check an make dir
check_and_make_d() {
    if [ ! -d "$1" ] 
    then
        mkdir -p $1 &> /dev/null
    fi
}

# create executable file
create_exec_file() {
    touch $SETUP_DIR$EXEC_F
    
    chmod +x $SETUP_DIR$EXEC_F
    
    echo $PREFIX_F > $SETUP_DIR$EXEC_F
    echo $SETUP_DIR$NAME "${setted_params[@]}" '$@' >> $SETUP_DIR$EXEC_F
}

# create link
create_link() {
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    ln -s $SETUP_DIR$EXEC_F $LINK_PATH$TAG_CHECKER &> /dev/null
}

#  build ver
build_ver() {
    branch=$($GIT rev-parse --abbrev-ref HEAD) &> /dev/null
    commits=$($GIT rev-list $branch --count) &> /dev/null
    last_author=$($GIT log -1 --pretty=format:"%an") &> /dev/null
    last_hash=$($GIT log -1 --pretty=format:"%h") &> /dev/null

    sed -Ei "s/current_commits/$commits/g" $SETUP_DIR$VERSION_FILE  &> /dev/null
    sed -i "s@beta@$branch@" $SETUP_DIR$VERSION_FILE  &> /dev/null
    sed -i "s@last_commiter@$last_author@" $SETUP_DIR$VERSION_FILE  &> /dev/null
    sed -i "s@last_hash@$last_hash@" $SETUP_DIR$VERSION_FILE  &> /dev/null
}

# check soft installed
check_soft() {
    # check pyton
    if ! which $PYTHON > /dev/null; then
        show_msg "Please, install python3 before using $0"
        exit 0
    fi

    # check git
    if ! which $GIT > /dev/null; then
        show_msg "Please, install git before using $0"
        exit 0
    fi
}

# main menu
main_menu() {
    main_menu_dlg=(--clear \
                   --title "Tag Checker Installer" \
                   --menu "Main menu" $wnd_sz_f)

    m_m_opts=(3 "Full install"
              4 "Full uninstall"
              5 "Upgrade files"
              6 "Change parameters"
              7 "Edit crontab"
              8 "Run from source"
              9 "Run from installed"
              10 "Exit from installer")

    clear
    choise=$("${dialog[@]}" "${main_menu_dlg[@]}" "${m_m_opts[@]}" 2>&1 >/dev/tty)
    clear
    case $choise in
        3 ) 
            full_install
            main_menu
            ;;
        4 ) 
            full_uninstall
            main_menu
            ;;
        5 ) 
            upgrade_files
            main_menu
            ;;
        6 ) 
            change_parameters
            accept_params
            show_msg "Parameters accepted. Use link: $TAG_CHECKER."
            clear
            main_menu
            ;;
        7 ) 
            edit_crontab
            main_menu
            ;;
        8 ) 
            run_from_source
            main_menu
            ;;
        9 ) 
            run_now
            main_menu
            ;;
        10 ) close_all_dialogs ;;
        255 ) close_all_dialogs ;;
        * ) close_all_dialogs ;;
    esac

    clear
}

upgrade_files() {
    upgrade_prog=(--gauge "Upgrade files..." $wnd_sz_g)

    clear
    (
        progress_step "Init updating files" 0

        progress_step "Remove $SETUP_DIR" 5
        check_and_rem_d "$SETUP_DIR"

        progress_step "make $SETUP_DIR." 15
        check_and_make_d "$SETUP_DIR"

        progress_step "Update files" 20
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${upgrade_prog[@]}" 2>&1 >/dev/tty)

    update_files

    (
        progress_step "Files was updated" 50
        progress_step "Finish updating files" 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${upgrade_prog[@]}" 2>&1 >/dev/tty)

    show_info "Files was updated."
}

# remove note from crontab
remove_from_crontab() {
    crontab -l | grep -q !"$NAME" > temp &> /dev/null
    crontab temp &> /dev/null
    rm temp &> /dev/null
}

# add note to crontab
add_to_crontab() {
    crontab -l > temp &> /dev/null
    echo "0 * * * * $SETUP_DIR$EXEC_F --update" >> temp &> /dev/null
    crontab temp &> /dev/null
    rm temp &> /dev/null
}

# edit crontab
edit_crontab() {
    crontab_menu_dlg=(--clear \
                      --title "Edit crontab" \
                      --menu "Actions" $wnd_sz_f)

    e_c_opts=(1 "Add to crontab."
              2 "Remove from crontab."
              3 "Skip.")

    clear
    choise=$("${dialog[@]}" "${crontab_menu_dlg[@]}" "${e_c_opts[@]}" 2>&1 >/dev/tty)
    clear
    case $choise in
        1 ) 
            remove_from_crontab
            add_to_crontab
            show_info "Note to crontab was added"
            ;;
        2 ) 
            remove_from_crontab 
            show_info "Note from crontab was deleted"
            ;;
        3 ) ;;
    esac

    clear
}

# update files
update_files() {
    update_f_prog=(--gauge "Update files..." $wnd_sz_g)

    clear
    (
        progress_step "Init updating files" 0

        progress_step "Script files was copied" 10
        yes | cp -rf $SRC_DIR* $SETUP_DIR &> /dev/null

        progress_step "Config file was checked." 15
        cp -rfn $CUR_DIR$CONFIG_FILE $CONFIG_DIR &> /dev/null
        chmod 777 $CONFIG_DIR$CONFIG_FILE &> /dev/null

        progress_step "Copy scripts" 20
        cp $CUR_DIR$SRC_DIR$MISC_DIR$SCRIPTS_FILE $OUT_DIR &> /dev/null

        progress_step "Copy styles" 25
        cp $CUR_DIR$SRC_DIR$MISC_DIR$STYLE_FILE $OUT_DIR &> /dev/null

        progress_step "Create build version" 50
        build_ver

        progress_step "Create exec file" 75
        create_exec_file

        progress_step "Create link" 90
        create_link

        progress_step "Finish updating files" 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${update_f_prog[@]}" 2>&1 >/dev/tty)

    clear
}

# delete dirs
delete_dirs() {
    del_dirs_dlg=(--gauge "Create dirs" $wnd_sz_g)
    (
        progress_step "remove $SETUP_DIR" 35
        check_and_rem_d "$SETUP_DIR"

        progress_step "remove $OUT_ORD_DIR" 75
        check_and_rem_d "$OUT_DIR"

        progress_step "remove $LOG_DIR" 100
        check_and_rem_d "$LOG_DIR"
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${del_dirs_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

# create dirs
create_dirs() {
    cr_dirs_dlg=(--gauge "Create dirs" $wnd_sz_g)
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
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${cr_dirs_dlg[@]}" 2>&1 >/dev/tty)

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
              5 "Out logs to stdout off." "${setted_params_sw[5]}"
              6 "Logging on." "${setted_params_sw[6]}")


    choises=$("${dialog[@]}" "${change_params_dlg[@]}" "${c_p_opts[@]}" 2>&1 >/dev/tty)

    for choise in $choises
    do
        case $choise in
            1) changed[1]="$sud" changed_sw[1]=$sw_on;;
            2) changed[2]="$mt" changed_sw[2]=$sw_on;;
            3) changed[3]="$deb" changed_sw[3]=$sw_on;;
            4) changed[4]="$tim" changed_sw[4]=$sw_on;;
            5) changed[5]="$quiet" changed_sw[5]=$sw_off;;
            6) changed[6]="$log" changed_sw[6]=$sw_on;;
        esac
    done

    setted_params=("${changed[@]}")
    setted_params_sw=("${changed_sw[@]}")

    clear
}

accept_params() {
    accept_params_dlg=(--gauge "Accept params..." $wnd_sz_g)
    (
        progress_step "Init create addition files" 0
        progress_step "Create exec file" 50
        create_exec_file

        progress_step "Create link" 100
        create_link
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${accept_params_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

show_msg() {
    msgbox_dlg=(--title "Message" --msgbox "$1" $wnd_sz)
    $("${dialog[@]}" "${msgbox_dlg[@]}" 2>&1 >/dev/tty)
    clear
}

show_info() {
    infobox_dlg=(--title "Info" --infobox "$1" $wnd_sz)
    $("${dialog[@]}" "${infobox_dlg[@]}" 2>&1 >/dev/tty)

    sleep 0.5
    clear
}

# run_from_source
run_from_source() {
    change_parameters

    $CUR_DIR$SRC_DIR$NAME "${setted_params[@]}" $quiet $log $sud $mt $deb $tim $UPDATE_A &> /dev/null

    show_info "Script from source was finish work."
}

progress_step() {
        echo $2

        echo "XXX"
        echo $1
        echo "XXX"

        sleep 0.1
}

# full install
full_install() {
    full_install_dlg=(--gauge "Full install..." $wnd_sz_g)
    (
        progress_step "Init installing \n fadas \n asdasd" 5
        
        progress_step "Create dirs" 35
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    create_dirs
    
    (
        progress_step "Update files" 65
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    update_files

    (
        progress_step "Change parameters" 80
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    change_parameters
    accept_params

    (
        progress_step "Edit crontab" 90
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    edit_crontab

    (
        progress_step "Finish installing" 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)
    
    clear
}

# full uninstall
full_uninstall() {
    full_uninstall_dlg=(--gauge "Full uninstall..." $wnd_sz_g)
    (
        progress_step "Init uninstalling" 5
        
        progress_step "Remove dirs" 40
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    delete_dirs

    (
        progress_step "Remove files" 70
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    remove_from_crontab

    (
        progress_step "Remove note from crontab" 90
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)


    (
        progress_step "Finish uninstalling" 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

# run installed now
run_now() {
    $TAG_CHECKER $UPDATE_A &> /dev/null

    show_info "installed script was finish work."
}

close_all_dialogs() {
    clear
    exit 0
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
