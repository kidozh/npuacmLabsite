# -*- coding: UTF-8 -*-
from peewee import *
from db.models import baseModel
import datetime





class studentInfo(baseModel):
    schoolChoice = (("1", "航空学院"),
                    ("2", "航天学院"),
                    ("3", "航海学院"),
                    ("4", "材料学院"),
                    ("5", "机电学院"),
                    ("6", "力学与土木建设学院"),
                    ("7", "动力与能源学院"),
                    ("8", "电子信息学院"),
                    ("9", "自动化学院"),
                    ("10", "计算机学院"),
                    ("11", "理学院"),
                    ("12", "管理学院"),
                    ("13", "人文与经法学院"),
                    ("14", "软件与微电子学院"),
                    ("15", "生命学院"),
                    ("16", "外国语学院"),
                    ("17", "国际教育学院"),
                    ("18", "保密学院"),
                    ("0", "教育实验学院"),
                    ("19", "其他学院/机构/附属中学"),
                    ('others', "外校")
                )

    genderChoices = (
        ('male', '男'),
        ('female', '妹纸'),
        ('dalao', '大佬')
    )

    name = CharField(max_length=20)
    stuID = CharField(max_length=20)
    college = CharField(max_length=50,choices=schoolChoice)
    gender = CharField(max_length=10,choices=genderChoices)
    university = CharField(max_length=100,default='NWPU')
    email = CharField(max_length=50)
    phone = CharField(max_length=16)
    registerTime = DateTimeField(default=datetime.datetime.now())
    isAuth = BooleanField(default=False)