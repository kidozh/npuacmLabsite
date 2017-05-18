__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

urlpatterns = [
    ('/','acmDetectInfo.view.queryRequestHandler'),
    ('/api/','acmDetectInfo.view.queryProcessHandler'),
    ('/api/test/','acmDetectInfo.view.multipleQueryHandler'),
    ('/realtime/','acmDetectInfo.view.echoProblemHandler'),
    ('/doc/(\w+)/','acmDetectInfo.view.docRequestHandler'),
    ('/bulk/','acmDetectInfo.view.bulkQueryRequestHandler'),
    ('/cron/','acmDetectInfo.view.cronQueryRequestHandler'),
    ('/cron/realtime/','acmDetectInfo.view.cronRealtimeRequestHandler'),
    ('/board/','acmDetectInfo.view.boardRequestHandler'),
    ('/update/manually/','acmDetectInfo.view.cronTestRequestHandler'),
]

# cron should be like (time,function)
from view import cronScan

cron = [
    (cronScan,60*60*1000)

]