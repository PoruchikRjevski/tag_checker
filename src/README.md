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
    
   
   
Order of doings:
- check if git installed
- read config.ini
- update repos by links in config
- get tags from develop branches
- configurate web pages for each department
- close all
    
    
    
repo_1
repo_2
repo_3
    
