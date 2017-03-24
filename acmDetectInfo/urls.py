__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

urlpatterns = [
    ('/','acmDetectInfo.view.queryRequestHandler'),
    ('/api/','acmDetectInfo.view.queryProcessHandler'),
    ('/api/test/','acmDetectInfo.view.multipleQueryHandler'),
    ('/realtime/','acmDetectInfo.view.echoProblemHandler'),
    ('/doc/(\w+)/','acmDetectInfo.view.docRequestHandler'),
    ('/bulk/','acmDetectInfo.view.bulkQueryRequestHandler'),
]