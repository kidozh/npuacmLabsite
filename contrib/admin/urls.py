# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from conf.urls import include
import contrib.admin.uimodule
from tornado.web import URLSpec,url

urlpatterns = [
    ('/','contrib.admin.view.adminManageHandler'),
    ('/login/','contrib.admin.view.authRequestHandler'),
    ('/manage/','contrib.admin.view.adminManageHandler'),
    ('/manage/(?P<modelName>.+)/data/','contrib.admin.view.appModelApiManager'),
    ('/manage/(?P<modelName>.+)/show/','contrib.admin.view.appModelManager'),
    ('/manage/(?P<modelName>.+)/add/','contrib.admin.view.appModelAddManager'),
    ('/manage/(?P<modelName>.+)/change/(?P<id>.+)/','contrib.admin.view.appModelChangeManager'),
    ('/manage/(?P<modelName>.+)/delete/(?P<id>.+)/','contrib.admin.view.appModelDeleteManager'),
    # monitor system
    ('/serverStatus','contrib.admin.view.statusAPIHandler'),
    ('/serverStatusWS','contrib.admin.view.statusWebsocketAPIHandler'),
    # chat channel so that administrator could chat realtime or record some data

]

UImodule = {
    'get_option':contrib.admin.uimodule.optionModule,
    'adminlte_load_left_sidebar':contrib.admin.uimodule.appModelModule
}

from contrib.admin.log import praseLog

# cron should be (func,every ms)

cron = [
    #(praseLog,10*60*1000)
]
