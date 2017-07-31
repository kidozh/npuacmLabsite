# -*- coding: UTF-8 -*-
# author = kidozh
from peewee import *
from db.models import baseModel
import datetime




class markdownNotice(baseModel):
    notice_type_choice = (
        ('draft', '草稿'),
        ('prerelease','预发布'),
        ('publish', '发布'),
        ('depreciate','废止'),
        ('delete','删除')
    )
    title = CharField(max_length=100)
    publish_time = DateTimeField(default=datetime.datetime.now)
    publish_status = CharField(choices=notice_type_choice,default='draft')
    markdown_cotent = TextField()
    is_top = BooleanField(default=False)
    pos_click = IntegerField(default=0)
    neg_click = IntegerField(default=0)
    view_num = IntegerField(default=0)

    valid_announcement_exist = BooleanField(default=False)
    valid_start_time = DateTimeField(null=True,default=datetime.datetime.now)
    valid_end_time = DateTimeField(null=True)

    # security module
    need_pass = BooleanField(default=False)
    password = CharField(null=True)

    def retrive_all_info(self):
        # for name,value in vars(self).items():
        #     print name,value
        return vars(self).items()[0][1]
        #return [(member_name,value) for member_name, value in vars(self).items()]
