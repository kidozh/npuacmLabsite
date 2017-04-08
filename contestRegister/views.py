# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from core.requestHandler import BaseHandler
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.websocket
import datetime
import urllib2
import json
import logging
import time
from .models import studentInfo

class portalRequestHandler(BaseHandler):
    def get(self):
        args = locals()
        args.pop('self')
        self.render('contestRegister/portal.html', **args)

class registerRequestHandler(BaseHandler):
    def get(self):
        args = locals()
        args.pop('self')
        self.render('contestRegister/register.html', **args)

    def post(self,*args,**kwargs):
        name = self.get_argument('name')
        stuID = self.get_argument('studentID')

        gender = self.get_argument('sex','female')
        if gender!= 'female':
            gender='male'
        email = self.get_argument('email')
        college = self.get_argument('school')
        phone = self.get_argument('phone')

        stuInfo = studentInfo(
            name=name,
            stuID=stuID,
            gender=gender,
            email=email,
            college=college,
            phone=phone
        )
        stuInfo.save()

        args = locals()
        args.pop('self')
        self.render('contestRegister/result.html', **args)