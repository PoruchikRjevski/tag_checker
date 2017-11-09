Order tag checker.

#### USER INFO ####
Issues:
- check tags in selected repo's at configuration file tag_checker.ini
- create web-pages with tables of info about tag's commits, dates etc


Dependency's:
- Python 3.4 or higher
- Git 2.14.1 or higher

Installing:
- git clone git@srv-swdev:/opensource/device_tag_visualiser.git
- cd device_tag_visualiser/
- git checkout develop
- sudo ./installer.py [install.sh - IS DEPRECATED FULLY]
- Installer points:
    - Install - full script installation(create dirs, copy sources, creating symlinks and adding task to crontab)
    - Uninstall - full uninstall(remove all with backup configs in /tmp/tag_checker_backups/
    - Update files - copy source, misc and reset version
    - Change run parameters - selecting script run params and recreate executables with symlinks
    - Backups - Control of config's backups
- two ways to edit config:
    - edit tag_checker.ini manually(example in config.example/)
    - edit by script controls(for help exec tag_checker -h)
- all actions you can find in menu install.sh

#### DEVELOPER INFO ####
Main parts:
- logger
- config loader(CfgLoader)
    - load config and put it to model
    - load mapped names of devices from tag_checker_translate
    - for even part [xxx] create dict and go to repo for check tags
- tag model(TagModel)
    - agregate all info about tags, repos, commits etc
- checker(GitMan)
    - got throw repos, update, get tags, parce it's put info to model
- web configurator(WebGen)
    - create web page's:
        - main - last changes for all departments, devices and types(ITEM, ORDER, ALL)
        - for every device
        - for every item number