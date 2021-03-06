# -*- coding: UTF-8 -*-
__author__ = 'kidozh'
from conf.urls import include

# This is the URL mapper which will assembly all the package
urlpatterns = [
    #(r"^/admin",include('contrib.admin.urls')),
    (r"^",include('acmDetectInfo.urls')),
    (r"^/about/", 'portal.view.portalHandler'),
    (r"^/doc", include('portal.urls')),
    # (r'^/about/','portal.view.aboutHandler'),
    (r"^/query",include('acmCralwer.urls')),
    (r"^/t",include('notification.urls')),
    (r"^/admin",include('contrib.admin.urls')),
    (r"^/plag",include('codePlag.urls')),
    (r'^/contest2017',include('contestRegister.urls')),
    (r'^/usefulTools',include('usefulTools.urls')),
    # need place last
    (r'(.*?)','portal.view.baseRedirectHandler')
]