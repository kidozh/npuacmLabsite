__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

# for template output
import tornado.template
import os
template_path = os.path.join(os.path.dirname(__file__), "templates")
template_loader = tornado.template.Loader(template_path)

from sqlalchemy.ext.declarative import declarative_base

# init configuration then get connect key
from db import connectHandler

connect = connectHandler()

base = declarative_base(bind=connect.engineHandler)

