# Introduction #

Software version installation history web visualization tool.

# User manual #

## Issues ##

- check tags in selected repo's at configuration file tag_checker.ini
- create web-pages with tables of info about tag's commits, dates etc

## Dependencies ##

- Python >= 3.4
- Git >= 2.14.1

## Installation ##

- Get code and install to system:
        $ git clone git@srv-swdev:/opensource/device_tag_visualiser.git
        $ cd device_tag_visualiser/
        $ git checkout develop
        # ./installer.py 
  WARNING: install.sh - IS DEPRECATED
- Installer points:
    - Install - full script installation(create dirs, copy sources, creating symlinks and adding task to crontab)
    - Uninstall - full uninstall(remove all with backup configs in /tmp/tag_checker_backups/
    - Update files - copy source, misc and reset version
    - Change run parameters - selecting script run params and recreate executables with symlinks
    - Backups - Control of config's backups
- there're two ways to edit config:
    - edit tag_checker.ini manually(example in config.example/)
    - edit by script controls(for help exec tag_checker -h)
- all available actions you can find in ui-menu of script "install.sh"

# Developer manual #

## Main modules ##

- logger
- config loader(CfgLoader)
    - load config and put it to model
    - load mapped names of devices from tag_checker_translate
    - for even part [xxx] create dict and go to repo for check tags
- tag model(TagModel)
    - aggregate all info about tags, repos, commits etc
- checker(GitMan)
    - got throw repos, update, get tags, parse it's put info to model
- web configurator(WebGen)
    - create web page's:
        - main - last changes for all departments, devices and types(ITEM, ORDER, ALL)
        - for every device
        - for every item number
        
## Hints ##

- use --cfg-dir option for run during debug to setup specific environment
    for example: 
        - create folders in <project_root_dir>:
            [.work/test]
                [config]
                [www]
                [log]
                [data]
        - create config file:
            <project_root_dir>/.work/test/config/config.ini
                [CONFIG]
                root_dir = ..
                out_dir = www
                log_dir = log
                data_dir = data
                ...
        - create new PyCharm configuration: 
            CWD:    <project_root_dir>
            PARAMS: -u -f ... --cfg-dir=.work/test/config
        