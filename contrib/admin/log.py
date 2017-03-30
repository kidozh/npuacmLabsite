# -*- coding: UTF-8 -*-
__author__ = 'kidozh'
# use conf.models.configOption for store data

from conf import ENVIRONMENT_VARIABLE
import os
# refer the setting modules
os.environ[ENVIRONMENT_VARIABLE] = 'setting'

from conf.models import configOption
from view import BaseHandler
from contrib.admin.models import log
#from .models import log
class log_praser(BaseHandler):
    # use BaseHandler to automatically loading
    def __init__(self,log_path='log/server.log'):
        # please keep sync with yaml
        self.log_path = log_path

    def get_lastest_log_offset(self):
        BaseHandler.prepare(self)
        lastest_log_offset,created = configOption.get_or_create(name='lastest_log_offset',
                                                                defaults={'value': '0'})
        if created:
            lastest_log_offset.value = '0'
            lastest_log_offset.save()
        BaseHandler.on_finish(self)
        return int(lastest_log_offset.value)

    def parase_log(self):
        import re
        import datetime
        latest_log_offset = self.get_lastest_log_offset()

        matchRegex = r'^(.+) - tornado\.(\w+) - (\w+) - (\d+) (\w+) (.*?) \((.*?)\) (.*?)ms'
        queryTimeRegex = r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+),(\d+)'
        compileRegex = re.compile(matchRegex)
        timeCompiledRegex = re.compile(queryTimeRegex)
        with open(self.log_path,'r+') as f:
            # move pointer to current offset
            f.seek(latest_log_offset,0)
            data_source = []
            for eachline in f.readlines():

                info =  compileRegex.findall(eachline)

                if len(info) == 1:
                    # extract info from length
                    timeString, logType, logLevel, requestStatus, requestType, requestURL, requestIP, requestDuration = info[0]
                    # need to praser timestring first
                    year,month,day,hour,minute,second,milsecond = timeCompiledRegex.findall(timeString)[0]
                    reqDatetime = datetime.datetime(int(year),
                                                    int(month),
                                                    int(day),
                                                    hour=int(hour),
                                                    minute=int(minute),
                                                    second=int(second),
                                                    microsecond=int(milsecond))

                    thisLineLog = dict(queryTime=reqDatetime, logType=logType, logLevel=logLevel,
                                       requestStatus=requestStatus, requestType=requestType, requestURL=requestURL,
                                       requestIP=requestIP, requestDuration=requestDuration)


                    data_source.append(thisLineLog)
                #print eachline
            cur_log_offset = f.tell()
            # print '# cur',cur_log_offset


            # store info
            BaseHandler.prepare(self)
            # bulk insert
            from db import database
            with database.atomic():
                for idx in range(0, len(data_source), 100):
                    log.insert_many(data_source[idx:idx+100]).execute()

            lastest_log_offset = configOption.get(name='lastest_log_offset')


            lastest_log_offset.value = cur_log_offset
            lastest_log_offset.save()
            # save time
            import time
            lastest_log_update_time,created = configOption.get_or_create(name='lastest_log_update_time',
                                                                defaults={'value': str(time.time())})
            lastest_log_update_time.value = str(time.time())
            lastest_log_update_time.save()
            BaseHandler.on_finish(self)

def praseLog():
    a = log_praser()
    a.parase_log()

if __name__ == '__main__':
    from conf import ENVIRONMENT_VARIABLE
    import os
    # refer the setting modules
    os.environ[ENVIRONMENT_VARIABLE] = 'setting'
    praseLog()

