# -*- coding: UTF-8 -*-
__author__ = 'kidozh'


import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.websocket
from core.requestHandler import BaseHandler

class portalHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('portal/index.html')

class aboutHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('portal/about.html')

class baseRedirectHandler(BaseHandler):
    def get(self, url,*args, **kwargs):
        if not url.endswith('/'):
            self.redirect(self.reverse_url('portal.view.baseRedirectHandler','%s/'%(url)))
        else:
            self._reason = '你好像来到了一个荒原？'
            self._status_code = 404
            self.write_error(404)


class staticNoticePage(BaseHandler):
    def get(self, pageName, *args, **kwargs):
        if pageName not in ['multi-server']:
            self.write_error(404)
            return
        try:
            self.render('portal/%s.html' % (pageName), *args)
        except Exception as e:
            raise e
            self._reason = '瞄~'
            self.write_error(404)