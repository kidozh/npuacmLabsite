__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

from peewee import *
from db.models import baseModel
import datetime

class accountProbRecord(baseModel):

    account = CharField(max_length=20)
    pojNum = IntegerField()
    hduNum = IntegerField()
    zojNum = IntegerField()
    cfNum  = IntegerField()
    vjudgeNum = IntegerField()

    queryTime = DateTimeField(default=datetime.datetime.now())