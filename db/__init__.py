# -*- coding: UTF-8 -*-
__author__ = 'kidozh'
# read the option of setting
from conf import setting,UserSettingsHolder

# for sqlalchemy
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# for sqlalchemy-utils
from sqlalchemy_utils import database_exists, create_database
import logging

# -----------------------------------------
#
# for peewee model
#
# -----------------------------------------



class connectHandler:
    def __init__(self):
        Setting = setting()
        Setting._setup()
        self.settingMapper = Setting._wrapped
        # configuration from setting
        # get configuration from setting
        # according to sqlalchemy we should form that address
        # dialect[+driver]://user:password@host/dbname
        self.DB_HOST = Setting._wrapped.DB_HOST
        self.DB_USER = Setting._wrapped.DB_USER
        self.DB_PASSWD = Setting._wrapped.DB_PASSWD
        self.DB_TYPE = Setting._wrapped.DB_TYPE
        self.DB_DRIVER = Setting._wrapped.DB_DRIVER
        self.DB_NAME = Setting._wrapped.DB_NAME

    @property
    def connectKey(self):
        if self.DB_DRIVER == '':
            # use default driver
            # use default utf8 to prevent encode characters error
            sqlAddress = '%s://%s:%s@%s/%s?charset=utf8' % (
            self.DB_TYPE, self.DB_USER, self.DB_PASSWD, self.DB_HOST, self.DB_NAME)
        else:
            sqlAddress = '%s+%s://%s:%s@%s/%s?charset=utf8' % (
            self.DB_TYPE, self.DB_DRIVER, self.DB_USER, self.DB_PASSWD, self.DB_HOST, self.DB_NAME)
        return sqlAddress

    @property
    def engineHandler(self):
        return create_engine(self.connectKey, echo=self.settingMapper.DEBUG)

    @property
    def isDataBaseExist(self):
        return database_exists(self.connectKey)

    def initDB(self):
        '''
        it will create the database and table automatically
        :return:
        '''
        # it will detect whether database is connecting, if not, it will create database automatically
        if not self.isDataBaseExist:
            try:
                create_database(self.connectKey)
            except:
                logging.critical('Database : %s is not exist or configuration is error' % (self.DB_NAME))

        # it will create table automatically
        Base = declarative_base()
        # auto-fit the table
        Base.metadata.create_all(engine)

        return True

    @property
    def gennerateSession(self):
        '''
        gennerate session for sqlalchemy in order to operate the database
        :return: sesscionmaker
        '''
        return sessionmaker(bind=self.engineHandler)




from db import connectHandler

connectDB = connectHandler()

from peewee import *
from playhouse.db_url import connect
database = connect(connectDB.connectKey)

base = declarative_base(bind=connectDB.engineHandler)

if __name__ == '__main__':
    import os
    from conf import ENVIRONMENT_VARIABLE
    import time

    clock = time.clock()
    os.environ[ENVIRONMENT_VARIABLE] = 'setting'
    a = connectHandler()
