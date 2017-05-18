# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

import os

import tornado.httpserver
import tornado.ioloop
import tornado.ioloop
import tornado.options
import tornado.web
import os

# import URL manually
from conf.urls import urlPackage,templateModuleFinder,periodTaskFinder

from tornado.options import options,define
# define the port in order to simplify debug mode

define("port", default=8000, help="run on the given port", type=int)
if __name__ == "__main__":

    # set environmental value for setting
    from conf import ENVIRONMENT_VARIABLE
    # refer the setting modules
    os.environ[ENVIRONMENT_VARIABLE] = 'setting'

    # parse command
    tornado.options.parse_command_line()

    # for URL configuration
    from conf import setting
    Setting = setting()
    Setting._setup()
    urlMapper = urlPackage(Setting._wrapped.ROOT_URLCONF)

    # for module configuration
    moduleFinder = templateModuleFinder()

    # create table and database
    # empty for extension


    # --------------------------------------------------
    #
    # for log configuration
    #
    # --------------------------------------------------
    if hasattr(Setting._wrapped, "LOGFILE") and Setting._wrapped.LOGFILE:
        import logging
        import yaml
        import logging.config
        from logging import StreamHandler
        from logging.handlers import RotatingFileHandler,SMTPHandler,TimedRotatingFileHandler

        logFilePath = Setting._wrapped.LOGFILE
        logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

        '''# file_handler = RotatingFileHandler(logFilePath, 'a',1 * 1024 * 1024, 10)

        # roll info at midnight
        file_handler = TimedRotatingFileHandler(logFilePath,when='midnight')

        RootLogger = logging.getLogger()

        # We have a File_handler so we don't need streamhandler
        for handler in RootLogger.handlers:
            # There are some Handler is a subclass of streamhandler
            # SO, using the type instead isinstance
            if type(handler) is StreamHandler:
                RootLogger.removeHandler(handler)

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))

        RootLogger.addHandler(file_handler)

        # mail

        if hasattr(Setting._wrapped, "MAIL_SERVER"):
            credentials = None
            if Setting._wrapped.MAIL_USERNAME and Setting._wrapped.MAIL_PASSWORD:
                credentials = (Setting._wrapped.MAIL_USERNAME, Setting._wrapped.MAIL_PASSWORD)
                mail_handler = SMTPHandler((Setting._wrapped.MAIL_SERVER,Setting._wrapped.MAIL_PORT),
                                            Setting._wrapped.MAIL_USERNAME,
                                            Setting._wrapped.ADMINS, "站点出错了！",
                                            credentials,secure=True)
                mail_handler.setLevel(logging.ERROR)
                RootLogger.addHandler(mail_handler)'''

    # -------------------------------------------
    #
    # end log module
    #
    # -------------------------------------------

    # setting
    settings = {
        "xsrf_cookies": True,
        "login_url": "/admin/login/",
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": Setting._wrapped.SECRET_KEY,
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "debug": Setting._wrapped.DEBUG,
    }

    app = tornado.web.Application(
        # get Exported URL
        handlers = urlMapper.detectURL(),
        # get Export UI modules
        ui_modules=moduleFinder.uiDict,
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(app,xheaders = True)
    http_server.listen(options.port)
    # import prase log

    # gather all cron
    cronFinder = periodTaskFinder()
    for (func,ms) in cronFinder.periodTask:
        print('[CRON] %s will recycle in every %s ' %(func,ms))
        tornado.ioloop.PeriodicCallback(func,ms).start()
    print('[CRON] all task is listed...')
    tornado.ioloop.IOLoop.instance().start()