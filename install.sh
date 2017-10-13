#!/bin/bash

# MAIN CONSTS
CUR_DIR="./"
LOG_DIR="/tmp/tag_checker_log/"
LINK_PATH="/usr/local/bin/"
SETUP_DIR="/opt/tag_checker/"
OUT_DIR="/var/www/swver_hist/"
OUT_DEV_DIR=$OUT_DIR"devices/"
OUT_ORD_DIR=$OUT_DEV_DIR"orders/"
CSS_DIR="css/"
JS_DIR="js/"
OUT_JS_DIR=$OUT_DIR$JS_DIR
OUT_CSS_DIR=$OUT_DIR$CSS_DIR
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

# PARAMETERS VARS
def_ar=("" "" "" "" "" "")

nums=('"1"' '"2"' '"3"' '"4"' '"5"' '"6"')

tag_params=("-s" "-m" "-d" "-t" "-q" "-l")

setted_params=("${def_ar[@]}")
setted_params_sw=("${def_ar[@]}")

# DIALOG VARS
DIALOG="dialog"
WHIPT="whiptail"

dialog=(dialog)

sw_on="on"
sw_off="off"

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

# MAIN FUNCS
main() {
    check_soft

    main_menu

    exit 0
}

check_soft() {
    # check dialog or whiptail
    if which $DIALOG > /dev/null; then
        dialog=($DIALOG)
    elif which $WHIPT > /dev/null; then
        dialog=($WHIPT)
    else
        echo "Please install whiptail or dialog(it is better)."
        exit 0
    fi

    # check pyton
    if ! which $PYTHON > /dev/null; then
        show_msg "Please, install python3 before using $0."
        exit 0
    fi

    # check git
    if ! which $GIT > /dev/null; then
        show_msg "Please, install git before using $0."
        exit 0
    fi
}

main_menu() {
    main_menu_dlg=(--clear \
                   --title "Tag Checker Installer" \
                   --menu "Main menu" $wnd_sz_f)

    m_m_opts=(1 "Install"
              2 "Uninstall"
              3 "Upgrade files"
              4 "Change parameters"
              5 "Edit crontab"
              6 "Run from source"
              7 "Run from installed"
              8 "Exit from installer")

    clear
    choise_p=$("${dialog[@]}" "${main_menu_dlg[@]}" "${m_m_opts[@]}" 2>&1 >/dev/tty)
    clear
    case $choise_p in
        1 ) 
            full_install
            main_menu
            ;;
        2 ) 
            full_uninstall
            main_menu
            ;;
        3 ) 
            upgrade_files
            main_menu
            ;;
        4 ) 
            change_parameters
            accept_params
            show_msg "Parameters accepted: ${setted_params[*]} . Use link: $TAG_CHECKER."
            clear
            main_menu
            ;;
        5 ) 
            edit_crontab
            main_menu
            ;;
        6 ) 
            run_from_source
            main_menu
            ;;
        7 ) 
            run_now
            main_menu
            ;;
        8 ) close_all_dialogs ;;
        255 ) close_all_dialogs ;;
        * ) close_all_dialogs ;;
    esac

    # clear
}

full_install() {
    full_install_dlg=(--gauge "Full install" $wnd_sz_g)
    (
        progress_step "Init installing..." 5
        
        progress_step "Creating dirs..." 35
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    create_dirs
    
    (
        progress_step "Updating files..." 65
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    update_files

    (
        progress_step "Changing parameters..." 80
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    change_parameters
    accept_params

    (
        progress_step "Editing crontab..." 90
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)

    edit_crontab

    (
        progress_step "Finishing installing..." 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_install_dlg[@]}" 2>&1 >/dev/tty)
    
    clear
}

create_dirs() {
    cr_dirs_dlg=(--gauge "Create dirs" $wnd_sz_g)
    (
        progress_step "making $SETUP_DIR ..." 25
        check_and_make_d "$SETUP_DIR"
        chmod +x $SETUP_DIR

        progress_step "making $OUT_ORD_DIR ..." 40
        check_and_make_d "$OUT_ORD_DIR"
        chmod +x $OUT_ORD_DIR*
        
        progress_step "making $OUT_CSS_DIR ..." 55
        check_and_make_d "$OUT_CSS_DIR"
        chmod +x $OUT_CSS_DIR*
        
        progress_step "making $OUT_JS_DIR ..." 75
        check_and_make_d "$OUT_JS_DIR"
        chmod +x $OUT_JS_DIR*

        progress_step "making $LOG_DIR ..." 100
        check_and_make_d "$LOG_DIR"
        chmod +x $LOG_DIR
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${cr_dirs_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

full_uninstall() {
    full_uninstall_dlg=(--gauge "Full uninstall" $wnd_sz_g)
    (
        progress_step "Uninstalling..." 5
        
        progress_step "Removing dirs..." 40
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    delete_dirs

    (
        progress_step "Removing files..." 70
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    check_and_rem_f "$CONFIG_DIR$CONFIG_FILE"
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    (
        progress_step "Removing note from crontab" 90
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    remove_from_crontab

    (
        progress_step "Finishing uninstalling..." 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${full_uninstall_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

delete_dirs() {
    del_dirs_dlg=(--gauge "Remove dirs" $wnd_sz_g)
    (
        progress_step "Removing dirs..." 0

        progress_step "removing $SETUP_DIR" 35
        check_and_rem_d "$SETUP_DIR"

        progress_step "removnig $OUT_ORD_DIR" 75
        check_and_rem_d "$OUT_DIR"

        progress_step "removing $LOG_DIR" 100
        check_and_rem_d "$LOG_DIR"
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${del_dirs_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

upgrade_files() {
    upgrade_prog=(--gauge "Upgrade files" $wnd_sz_g)

    clear
    (
        progress_step "Updating files..." 0

        progress_step "Remove $SETUP_DIR" 5
        check_and_rem_d "$SETUP_DIR"

        progress_step "make $SETUP_DIR." 15
        check_and_make_d "$SETUP_DIR"

        progress_step "Update files" 20
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${upgrade_prog[@]}" 2>&1 >/dev/tty)

    update_files

    (
        progress_step "Files was updated" 50
        progress_step "Finishing updating files..." 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${upgrade_prog[@]}" 2>&1 >/dev/tty)

    show_info "Files was updated."
}

update_files() {
    update_f_prog=(--gauge "Update files" $wnd_sz_g)

    clear
    (
        progress_step "Init updating files..." 0

        progress_step "Source files was copied..." 10
        yes | cp -rf $SRC_DIR* $SETUP_DIR

        progress_step "Config file was checked..." 15
        cp -rfn $CUR_DIR$CONFIG_FILE $CONFIG_DIR
        chmod 777 $CONFIG_DIR$CONFIG_FILE
        
        progress_step "CSS files was copied..." 20
        yes | cp -rf $CUR_DIR$SRC_DIR$MISC_DIR$CSS_DIR* $OUT_DIR$CSS_DIR
        
        progress_step "JS files was copied..." 30
        yes | cp -rf $CUR_DIR$SRC_DIR$MISC_DIR$JS_DIR* $OUT_DIR$JS_DIR

        progress_step "Create build version..." 50
        build_ver

        progress_step "Accept params..." 75
        accept_params

        progress_step "Finishing updating files..." 100
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${update_f_prog[@]}" 2>&1 >/dev/tty)

    clear
}

build_ver() {
    branch=$($GIT rev-parse --abbrev-ref HEAD)
    commits=$($GIT rev-list $branch --count)
    last_author=$($GIT log -1 --pretty=format:"%an")
    last_hash=$($GIT log -1 --pretty=format:"%h")

    sed -Ei "s/current_commits/$commits/g" $SETUP_DIR$VERSION_FILE
    sed -i "s@beta@$branch@" $SETUP_DIR$VERSION_FILE
    sed -i "s@last_commiter@$last_author@" $SETUP_DIR$VERSION_FILE
    sed -i "s@last_hash@$last_hash@" $SETUP_DIR$VERSION_FILE
}

get_num() {
    i=1

    for num in ${nums[*]}
    do
        if [ "$num" == "$1" ]; then
            break
        fi
        ((i++))
    done

    return $i
}

change_parameters() {
    changed=("${def_ar[@]}")
    changed_sw=("${def_ar[@]}")

    c_p_opts=("1" "ON SUDO" "${setted_params_sw[1]}"
              "2" "ON MULTITHREADing" "${setted_params_sw[2]}"
              "3" "ON DEBUG out" "${setted_params_sw[3]}"
              "4" "ON TIMINGS calc" "${setted_params_sw[4]}"
              "5" "OFF use STDOUT" "${setted_params_sw[5]}"
              "6" "ON LOGging" "${setted_params_sw[6]}")


    choises=$("${dialog[@]}" "${change_params_dlg[@]}" "${c_p_opts[@]}" 3>&1 1>&2 2>&3)
    clear

    for choise in $choises
    do
        if [ $dialog == $WHIPT ]; then
            get_num $choise
            choose=$?
        else
            choose=$choise
        fi

        changed[$choose]="${tag_params[$(($choose-1))]}"
        if [ $choose == 5 ]; then
            changed_sw[$choose]=$sw_off
        else
            changed_sw[$choose]=$sw_on
        fi
    done

    setted_params=("${changed[@]}")
    setted_params_sw=("${changed_sw[@]}")
}

accept_params() {
    accept_params_dlg=(--gauge "Accept params" $wnd_sz_g)
    (
        progress_step "Init create addition files..." 0
        progress_step "Create exec file..." 50
        create_exec_file

        progress_step "Create link..." 100
        create_link
    ) | $("${dialog[@]}" "${progress_dlg[@]}" "${accept_params_dlg[@]}" 2>&1 >/dev/tty)

    clear
}

create_exec_file() {
    touch $SETUP_DIR$EXEC_F
    
    chmod +x $SETUP_DIR$EXEC_F
    
    echo $PREFIX_F > $SETUP_DIR$EXEC_F
    echo $SETUP_DIR$NAME "${setted_params[*]}" '$@' >> $SETUP_DIR$EXEC_F
}

create_link() {
    check_and_rem_f "$LINK_PATH$TAG_CHECKER"

    ln -s $SETUP_DIR$EXEC_F $LINK_PATH$TAG_CHECKER
}

edit_crontab() {
    crontab_menu_dlg=(--clear \
                      --title "Edit crontab" \
                      --menu "Actions" $wnd_sz_f)

    e_c_opts=(1 "ADD to crontab"
              2 "REMOVE from crontab"
              3 "SKIP")

    clear
    choise_cron=$("${dialog[@]}" "${crontab_menu_dlg[@]}" "${e_c_opts[@]}" 2>&1 >/dev/tty)
    clear
    case $choise_cron in
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

remove_from_crontab() {
    crontab -l | grep -q !"$NAME" > temp
    crontab temp
    rm temp
}

add_to_crontab() {
    crontab -l > temp
    echo "0 * * * * $SETUP_DIR$EXEC_F --update" >> temp
    crontab temp
    rm temp
}

run_from_source() {
    change_parameters

    $CUR_DIR$SRC_DIR$NAME "${setted_params[@]}" $UPDATE_A

    show_info "Script from source was finish work."
}

run_now() {
    $TAG_CHECKER $UPDATE_A

    show_info "installed script was finish work."
}

# AUX FUNCS
check_and_rem_f() {    
    if [ -f "$1" ] 
    then
        rm -f $1
    fi
}

check_and_rem_d() {    
    if [ -d "$1" ] 
    then
        rm -rf $1
    fi
}

check_and_make_d() {
    if [ ! -d "$1" ] 
    then
        mkdir -p $1
    fi
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

progress_step() {
        echo $2

        echo "XXX"
        echo $1
        echo "XXX"

        sleep 0.1
}

close_all_dialogs() {
    clear
    exit 0
}


# ENTER POINT
main
