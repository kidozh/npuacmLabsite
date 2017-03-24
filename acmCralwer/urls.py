__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

from conf.urls import include

urlpatterns = [
    ('/','acmCralwer.view.queryIndexHandler'),
    ('/api/','acmCralwer.view.queryInfoHandler'),
    ('/realtime/','acmCralwer.view.echoProblemHandler')
]