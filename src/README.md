Production tag checker.

Issues:
- check tags in selected repo's in confing.ini
- create web-pages with tables of info about tag's commits, dates etc


Main parts:
- logger
- config loader
    - load config from config.ini
    - for even part [xxx] create dict and go to repo for check tags
    - 
- checker
    - departmens(dep_num , repos) - dict
    - repos(repo_link) - list
    - apparats(app_1, app_2, app_3) - list
    - app_1(app_name, order_num, date, hash) - tuple
- web_configurer
    - create web page for each one of departments
    \\



Model:
- department
    - repos
        -repo
            - last tag
                - item
                - order num
                - date
                - hash
            - history tag
            - link

departments     - dict      - (dep_num, repos)
repos           - list      - (repo, ...)
repo            - tuple     - (last, history, link)
last            - tuple     - (item, order_num, date, comm_hash)
history         - list      - (tag, ...)


Order of doings:
+ init logger
+ check if git installed
+ read config file to model
+ update repos by links in config
- get tags from develop branches
- configurate web pages for each department
- close all
    

Git commands:
check branch: 								git branch
if not develop try switch to develop: 		git checkout develop
update repo:                                git update ... TODO
get all tags: 								git tag
for each tag get ref:						git rev-parse --short $TAG
    
    
repo_1
repo_2
repo_3
    
