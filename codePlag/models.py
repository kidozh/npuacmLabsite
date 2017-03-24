# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from peewee import *
from db.models import baseModel
import datetime

codeTypeChoice = (
    ('c/c++','C或者C++'),
    ('char','基本字符')
)

class codePlagRecord(baseModel):
    """
    a code plagiarism for check A and B
    """
    codeA = TextField()
    codeB = TextField()
    submit_time = DateTimeField(default=datetime.datetime.now,help_text=u'注册时间')
    # for similarity Check
    similarityA2B = FloatField(default=0.0)
    similarityB2A = FloatField(default=0.0)
    tokenLenA = IntegerField()
    tokenLenB = IntegerField()
    shareTokenLen = IntegerField()
    codeType = CharField(choices=codeTypeChoice,default='char')
    # prevent some sensitive words from showing
    visible = BooleanField(default=True)

class filePermitArchive(baseModel):
    """
    storage permit for using file scan
    """
    email = CharField(max_length=100,unique=True)
    auth_key = CharField(max_length=50)
    # only allow submit for 10 times
    plagFreq = IntegerField(default=10)

    # auth models
    isAuth = BooleanField(default=False)
    isBanned = BooleanField(default=False)
    submit_time = DateTimeField(default=datetime.datetime.now,help_text=u'注册时间')

class fileArchive(baseModel):
    """
    storage file archive
    """
    zipFilePath = CharField(max_length=512)
    extractFilePath = CharField(max_length=512)
    resultFilePath = CharField(max_length=512)
    storageInfo = TextField(null=True)
    fileTitle = CharField(max_length=100)

    fileUUID = CharField(max_length=50)
    codeType = CharField(max_length=50)
    # aviod pk
    issuedEmail = CharField(max_length=100)
    submit_time = DateTimeField(default=datetime.datetime.now,help_text=u'注册时间')