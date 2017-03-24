# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

urlpatterns = [
    ('/','codePlag.view.plagPortalRequestHandler'),
    ('/single/','codePlag.view.checkerRequestHandler'),
    ('/doc/(\w+)/','codePlag.view.docRequestHandler'),
    ('/file/','codePlag.view.fileCheckerRequestHandler'),
    ('/jplagFile/','codePlag.view.jplagCheckerRequestHandler'),
    ('/jplagFileArchive/','codePlag.view.fileArchiveQueryRequestHandler'),
    ('/register/','codePlag.view.accessUserRegisterRequestHandler'),
    ('/auth/(.*?)/','codePlag.view.authRequestHandler'),
    ('/export/(.*?)/(.*?)/','codePlag.view.exportJplagData'),

]