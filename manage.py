__author__ = 'kidozh'
# -*- coding: UTF-8 -*-
import os
from conf import ENVIRONMENT_VARIABLE
os.environ[ENVIRONMENT_VARIABLE] = 'setting'

from contrib.admin.appModel import modelFinder
from db import database

import sys


modelsFinder = modelFinder()
# a tuple containing three element : app,className,class
modelsList = modelsFinder.getInstalledModel()
models = [model for name,package in modelsList for dname,model in package if model!= []]
print models
print database.create_tables(models,safe=True)
