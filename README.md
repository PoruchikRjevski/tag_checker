Order tag checker.

#### USER INFO ####
Issues:
- check tags in selected repo's at configuration file tag_checker.ini
- create web-pages with tables of info about tag's commits, dates etc


Installing:
- git clone git@srv-swdev:/opensource/device_tag_visualiser.git
- cd device_tag_visualiser/
- git checkout develop
- sudo ./install.sh
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