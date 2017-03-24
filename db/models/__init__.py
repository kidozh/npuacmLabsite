# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from peewee import *
from db import database

class baseModel(Model):
    '''
    use for model
    '''
    class Meta:
        '''
        configure for database
        '''
        database = database