# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

# peewee setting
from db.models import baseModel
from peewee import *


class configOption(baseModel):
    '''
    this is option for configuration in template rendering and data rewrite like wp_option
    '''

    name = CharField(100,unique=True)
    value = CharField(100,null=True)

# Choice tuple contains a tuple (realValue,ShownText)
targetChoice = (
    ('_blank','在新窗口中打开被链接文档。'),
    ('','在本窗口之中打开窗口'),
)

class friendLinks(baseModel):
    '''
    This is friend link for global site
    '''
    url = CharField(max_length=255,help_text='显示的URL')
    name = CharField(max_length=255,help_text='显示的名称')
    target = CharField(choices=targetChoice,max_length=255,help_text='显示的Target项',default='')
    description = CharField(max_length=255,help_text='URL说明')
    visible = BooleanField(default=True)