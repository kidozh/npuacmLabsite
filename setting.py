# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

import os

# keep in secret all the time
SECRET_KEY = ')ac#4j9=^i7!5drrf)36r50!ot$4xa2%(v58a'

# host for database
DB_HOST = '127.0.0.1'

# username for database
DB_USER = 'root'

# password for database
DB_PASSWD = '8520967123'

# database's type
DB_TYPE = 'mysql'

# driver for SQLalchemy
DB_DRIVER = ''

# which database we should choose
DB_NAME = 'test'

# for installed Apps we will search these string then
INSTALLED_APPS = (
    'acmCralwer',
    'contrib.admin',
    'conf',
    'acmDetectInfo',
    'codePlag',
    'contestRegister',
    'usefulTools'
)

# for root urls
ROOT_URLCONF = 'urls'

# for log file
# LOGFILE = 'log/site.log'
LOGFILE = False

# for mail
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USERNAME = "noreply@npuacm.info"
MAIL_PASSWORD = ""

# administrator list
ADMINS = ["kidozh@kidozh.com", ]

# set debug value according to system type
if os.environ.get('OS') == 'Windows_NT':
    DEBUG = True

    LOGFILE = 'log/site.log'
    #LOGFILE = False

else:
    DEBUG = False
    DB_PASSWD = '8520967123'
    LOGFILE = 'log/site.log'


    DB_NAME = 'npuacm'

# for timezone
USE_TZ = True

TIME_ZONE = 'Asia/Shanghai'
