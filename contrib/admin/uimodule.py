# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

import tornado.web
import re

class optionModule(tornado.web.UIModule):
    def render(self,option):
        from conf.models import configOption
        from db import database
        flag = False
        try:
            database.connect()
        except:
            flag = True
            pass
        if configOption.select().where(configOption.name == option).exists():
            if not flag:
                database.close()
            return configOption.get(configOption.name == option).value

        else:
            if not flag:
                database.close()
            return ''

class appModelModule(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        from contrib.admin.appModel import modelFinder
        modelsFinder = modelFinder()
        # a tuple containing three element : app,className,class
        modelsList = modelsFinder.getInstalledModel()
        args = locals()
        args.pop('self')
        return self.render_string('contrib/admin/leftSideBar.html',**args)