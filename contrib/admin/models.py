# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from . import base
import datetime
import bcrypt
from exceptions import ImproperlyPassword
from peewee import *
from db.models import baseModel
from playhouse.fields import PasswordField


class admin(baseModel):
    username = CharField(unique=True)
    nickname = CharField(max_length=20,help_text=u'将会对外显示',null=True)
    password = PasswordField(help_text=u'采用bcrypt加密')

    # time
    register_time = DateTimeField(default=datetime.datetime.now,help_text=u'注册时间')

    # permissions
    isStaff = BooleanField(default=False,help_text=u'是否能登陆至仪表盘')
    isAdmin = BooleanField(default=False,help_text=u'是否能具有管理员权限')

    def authPassword(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')) and len(password) > 8


class log(baseModel):
    queryTime = DateTimeField(default=datetime.datetime.now)
    logType = CharField(max_length=20)
    logLevel = CharField(max_length=10)
    requestStatus = SmallIntegerField()
    # GET or POST
    requestType = CharField(max_length=8)
    requestURL = TextField()
    requestIP = CharField(max_length=20)
    requestDuration = FloatField()
