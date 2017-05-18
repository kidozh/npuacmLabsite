# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from peewee import *
from db.models import baseModel
import datetime

class acRecordArchive(baseModel):
    """
    archive record for ac
    """
    name = CharField(max_length=100)
    queryTime = DateTimeField(default=datetime.datetime.now())
    pojNum = IntegerField()
    hduNum = IntegerField()
    zojNum = IntegerField()
    cfNum = IntegerField()
    acdreamNum = IntegerField()
    bzojNum = IntegerField()
    otherOJNum = IntegerField()
    totalNum = IntegerField()
    # non-ac archive
    submitNum = IntegerField()
    ratio = FloatField()

class cronInfo(baseModel):
    email = CharField(max_length=50)
    account = CharField(max_length=30)
    isPermit = BooleanField(default=True)
    freezeDay = IntegerField(default=0)
    createTime = DateTimeField(default=datetime.datetime.now())