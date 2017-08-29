Order tag checker.

#### USER INFO ####
Issues:
- check tags in selected repo's at configuration file tag_checker.ini
- create web-pages with tables of info about tag's commits, dates etc


Installing:
- git clone git@srv-swdev:/opensource/device_tag_visualiser.git
- git checkout develop
- go to dir tag_checker
- edit tag_checker.ini
- edit tag_checker_translate
- run install.sh
- go throw menu
- if need - change in install.sh cron timeout update

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

Used git commands:
GIT_VER         = "git --version"                           # get git ver
CUR_BRANCH      = "git rev-parse --abbrev-ref HEAD"         # get current branch
SW_BRANCH       = "git checkout "                           # switch branch to
UPD_REPO        = "git pull"                                # update repo
GET_TAGS        = "git tag"                                 # get all tags for cur branch
GET_TAG_SSHA    = "git rev-parse --short "                  # get short SHA1 for tagged commit
GET_COMM_DATE   = "git show -s --format=%cd --date=short "  # get commit date by hash
GET_COMM_INFO   = "git log -{0!s} --format='{1!s}' "        # get commit info