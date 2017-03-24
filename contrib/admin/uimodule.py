# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

import tornado.web
import re
class urlModule(tornado.web.UIModule):
    def render(self,uimodule,*args,**kwargs):
        from conf.urls import urlPackage
        from conf import setting
        import tornado.web
        Setting = setting()
        Setting._setup()

        urlMapper = urlPackage(Setting._wrapped.ROOT_URLCONF)
        urlHandler = urlMapper.detectURL()
        for it in urlHandler:
            if isinstance(it,tornado.web.URLSpec):
                url = it._path
                moduleStr = it.handler_class.__name__
            else:
                url,moduleStr = it
            if moduleStr == uimodule:
                # filter invalid characters
                purifyURL = re.match(r'\W+(/.+)$',url)
                regexURL = purifyURL.group(1)
                u = tornado.web.URLSpec(regexURL,None)
                print args,kwargs,u.reverse(**kwargs)
                return u.reverse(**kwargs)
                # return purifyURL.group(1)
        return ''

class optionModule(tornado.web.UIModule):
    def render(self,option):
        from conf.models import configOption
        from db import database
        database.connect()
        if configOption.select().where(configOption.name == option).exists():
            database.close()
            return configOption.get(configOption.name == option).value

        else:
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