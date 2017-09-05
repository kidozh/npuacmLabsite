__author__ = 'kidozh'
# -*- coding: UTF-8 -*-
import tornado.web
import tornado
from db import connectHandler, database
from contrib.admin.models import *
import datetime

class BaseHandler(tornado.web.RequestHandler):
    # peewee
    def prepare(self):
        try:
            database.connect()
        except:
            pass
        return super(BaseHandler, self).prepare()

    def on_finish(self):
        # save to database...
        browser_log = log(
            logLevel='INFO',
            logType='access',
            requestStatus=self.get_status(),
            requestType=self.request.method,
            requestURL=self.request.uri,
            requestIP=self.request.remote_ip,
            requestDuration=1000.0 * self.request.request_time()
        )
        browser_log.save()

        if not database.is_closed():
            database.close()
        return super(BaseHandler, self).on_finish()

    def get_current_user(self):
        # check current user privilege
        username = self.get_secure_cookie("username")
        # init database connect

        # queryObj = connectInstance.query(adminUser).filter(adminUser.username == username)
        if admin.select().where(admin.username == username).exists():
            # there is a username
            aimUser = admin.select().where(admin.username == username).get()
            if aimUser.isStaff:
                # successfully
                self._current_user = aimUser
                return aimUser

        return None

    def write_error(self, status_code, **kwargs):
        args = locals()
        args.pop('self')
        self.render('error.html', **args)