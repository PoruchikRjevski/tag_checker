#!/usr/bin/bash

# show info
show_info() {
    echo "Set argument:"
    echo "1 - path to *.ini"
    echo "2 - mode:"
    echo "        - depends"
    echo "        - subdirs"
    echo "        - config"
}

# ---------------------------------
# checks
# ---------------------------------
# check entered dir with .pro files
if [[ $# -eq 0 ]] ; then
    show_info
    exit 0
fi

# ---------------------------------
# main loop
# ---------------------------------
if [[ $# -eq 2 ]] ; then
    ## prepare
    create_temp_d
    find_pro_files
    separate_names
    
    clear_temp_files
    
    case $2 in
    $MAIN_DEPENDS )
        get_depends
        build_dot $DEP_DOT
        build_png $DEP_PNG $DEP_DOT 
        show_me_the_money $CUR_DIR/$DEP_PNG
    ;;
    $MAIN_SUBDIRS )
        get_depends_ext $ATTR_SUBDIRS
        build_dot $SUBD_DOT
        build_png $SUBD_PNG $SUBD_DOT
        show_me_the_money $CUR_DIR/$SUBD_PNG
    ;;
    $MAIN_CONFIG )
        get_depends_ext $ATTR_CONFIG
        build_dot $CONF_DOT
        build_png $CONF_PNG $CONF_DOT
        show_me_the_money $CUR_DIR/$CONF_PNG
    ;;
    * )
        show_info
    ;;
    esac

    remove_temp_d
fi
