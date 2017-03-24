# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

'''

a new method to detect ACM problem in more efficient way

'''


from core.requestHandler import BaseHandler
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.websocket
import datetime
import urllib2
import json
import logging
import time
from .models import acRecordArchive

class queryRequestHandler(BaseHandler):
    def get(self,*args, **kwargs):
        args = locals()
        args.pop('self')
        self.render('queryProbInfo/portal.html',**args)

    def post(self,*args,**kwargs):
        name = self.get_argument("name")
        args = locals()
        args.pop('self')
        if authName(name) == None:
            self._reason = '错误的用户名'
            self.write_error(500)
            return None
        self.render('queryProbInfo/queryProcess.html',**args)

def authName(name):
    '''
        just a regex function to detect whether queryName is correct.
        :param queryName: name that waiting for detect
        :return: boolean value whether name is valid or not.
    '''
    import re
    return re.match(r'^[A-Za-z_0-9]+$', name)

class queryProcessHandler(BaseHandler):

    # for websocket
    def sendRealTimeInfo(self,oj,status,name,ac,submit,*args):
        # revInfo is for authenticate
        revInfo ={
            'mainName':self.mainName,
            'revKey':self.revKey,
            'queryTime':self.timestamp

        }
        # infoDict is for rendering
        import time
        queryTime = time.time()
        infoDict = {
            'oj':oj,
            'status':status,
            'ac':ac,
            'submit':submit,
            'name':name,
            'extra':args,
            'queryTime':queryTime,
        }
        try:
            echoProblemHandler.sendInfo(revInfo,infoDict)
            return  True
        except Exception as e:
            logging.error('Sending websocket is fail')
            return False

    @tornado.gen.coroutine
    def post(self,*args,**kwargs):
        import json
        name = self.get_argument("name")
        revKey = self.get_argument('revKey')
        timestamp =self.get_argument('timestamp')
        # for websocket auth
        self.timestamp = timestamp
        self.revKey = revKey
        self.name = name
        if authName(name) == None:
            self._reason = '错误的用户名'
            self.write_error(500)
            return
        import probCrawler
        query = probCrawler.crawler(queryName=name)
        client = tornado.httpclient.AsyncHTTPClient()
        # traverse non-auth oj rule
        for oj,website,acRegex,submitRegex in query.getNoAuthRules():
            success = False
            otherInfo = 0
            # build the URL
            url = website %name
            req = tornado.httpclient.HTTPRequest(url,headers=query.headers,request_timeout=5)
            # async
            response =yield tornado.gen.Task(client.fetch,req)
            if response.code == 200:
                success = True
                res = query.actRegexRules(response.body,acRegex,submitRegex,oj)
                for oj,ac,submit in res:
                    # should return True
                    self.sendRealTimeInfo(oj,success,name,ac,submit)
            else:
                # should return failure
                self.sendRealTimeInfo(oj,success,name,0,0)
                pass

        # edit for manually process
        # uestc
        oj = 'uestc'
        success = False
        URL = 'http://acm.uestc.edu.cn/user/userCenterData/%s' %name
        response = yield tornado.gen.Task(client.fetch,URL,headers=query.headers)
        if response.code == 200:
            res = query.getAsyncUestc(response.body)
            success = True
            for oj,ac,submit in res:
                self.sendRealTimeInfo(oj,success,name,ac,submit)
        else:

            query.wrongOJ[oj] = name
            self.sendRealTimeInfo(oj,success,name,0,0)
            pass

        # acdream
        oj = 'acdream'
        success = False
        acdreamURL = 'http://acdream.info/user/%s' % name
        response = yield tornado.gen.Task(client.fetch, acdreamURL, headers=query.headers)
        if response.code == 200:
            success = True
            res = query.getAsyncACdream(response.body)

            for oj,ac,submit in res:
                self.sendRealTimeInfo(oj,success,name,ac,submit)
        else:
            query.wrongOJ[oj] = name
            self.sendRealTimeInfo(oj,success,name,0,0)

        # codeforces
        oj = 'codeforces'
        query.acArchive[oj] = set()
        loopFlag = True
        loopTimes = 0
        count = 1000
        startItem = 1+loopTimes*count
        endItem = (loopTimes+1)*count
        # loop start
        ac = 0
        submit = 0
        t0 = time.time()
        while loopFlag:
            '''
            use cycle to travel the information
            '''
            loopTimes+=1
            website = 'http://codeforces.com/api/user.status?handle=%s&from=%s&count=%s' %(name,startItem,endItem)
            # try to get information
            startItem = 1 + loopTimes * count
            endItem = (loopTimes + 1) * count
            # updating data...
            try:
                # use async to rewrite the getting process
                req = tornado.httpclient.HTTPRequest(website,headers=query.headers,request_timeout=5)
                #jsonString = urllib2.urlopen(website).read()
                response =  yield tornado.gen.Task(client.fetch,req)
                if response.code == 200:
                    jsonString = response.body
            except:
                query.wrongOJ[oj] = name
                break
            data = json.loads(jsonString)
            if data[u'status'] == u'OK':
                if len(data[u'result']) == 0:
                    break
                else:
                    pass
                # store the submit number
                query.submitNum[oj] += len(data[u'result'])
                submit += len(data[u'result'])
                for i in data[u'result']:
                    # only accept AC problem
                    if i[u'verdict'] == 'OK':
                        problemInfo = i[u'problem']
                        problemText ='%s%s' %(problemInfo[u'contestId'],problemInfo[u'index'])
                        # append set
                        query.acArchive[oj].add(problemText)
                        ac += 1
                    else:
                        pass
            else:
                break

        self.sendRealTimeInfo(oj,True,name,ac,submit)

        # vjudge
        URL = 'https://vjudge.net/user/solveDetail/%s' %name
        response = yield tornado.gen.Task(client.fetch,URL,headers=query.headers)
        if response.code == 200:
            res = query.paraseVjudgeJSON(response.body)
            for oj,ac,submit in res:
                self.sendRealTimeInfo(oj,True,name,ac,submit)
        else:
            # rewrite this

            query.wrongOJ[oj] = name
            self.sendRealTimeInfo(oj,False,name,0,0)
            pass

        # prepare the json
        dataDict = {}
        dataDict['ac'] = query.acArchive
        for key, value in query.acArchive.items():
            if key:
                try:
                    dataDict['ac'][key] = list(value)
                except Exception as e:
                    logging.error(e)
                    pass
            else:
                pass
        dataDict['submit'] = query.submitNum
        dataDict['wrongOJ'] = query.wrongOJ
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(dataDict))
        self.finish()




class echoProblemHandler(tornado.websocket.WebSocketHandler):
    clients = []
    '''
    client is a dict that contains:
    mainName:''
    renderTime:a timestamp that renders web.
    '''
    cache = []
    cache_size = 200

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        msgDict = {}
        # 0 : connect start
        # 1 : right ,give answer
        # 2 : wrong , give reason
        # 3 : shutdown websocket
        if len(self.clients)>self.cache_size:
            echoProblemHandler.update_cache()
        else:
            pass
        msgDict['result'] = 0
        # response Text
        msgDict['response-Text'] = 'Websocket成功连接'
        msgDict['response-Time'] = ''
        self.write_message(json.dumps(msgDict))
        # echoProblemHandler.clients.add(self)


    def on_message(self, message):
        '''
        recieve the message and record one
        :param message: a JSON that have those things
        :return:
        '''

        msgDict={}
        # 0 : connect start
        # 1 : right ,give answer
        # 2 : wrong , give reason
        # 3 : shutdown websocket
        try:
            msgDict = {'result': 0, 'responseText': 'Websocket成功连接', 'responseTime': ''}
            # response Text
            self.write_message(json.dumps(msgDict))

            userInfo = json.loads(message)
            # now record this info
            infoDict = {'mainName': userInfo['mainName'],
                        'queryTime': userInfo['queryTime'], 'revKey': userInfo['revKey'], 'echoHandler': self}

            self.clients.append(infoDict)
        except Exception as e:
            print e
            msgDict = {}
            msgDict['result'] = 2
            # response Text
            msgDict['response-Text'] = 'Websocket连接失败'
            msgDict['response-Time'] = ''
            self.write_message(json.dumps(msgDict))


    def on_close(self):
        #msgDict = {'result': 3, 'response-Text': 'GoodBye~', 'response-Time': ''}
        # 0 : connect start
        # 1 : right ,give answer
        # 2 : wrong , give reason
        # 3 : shutdown websocket
        # response Text
        #self.write_message(json.dumps(msgDict))
        for client in self.clients:
            if client['echoHandler'] == self:
                self.clients.remove(client)
            else:
                pass

    @classmethod
    def update_cache(cls):
        # cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def sendInfo(cls,revInfo,infoDict):
        if isinstance(infoDict,dict) and isinstance(revInfo,dict):
            # search for relative client
            for client in cls.clients:
                if client['mainName'] == revInfo['mainName'] \
                and str(client['queryTime']) == str(revInfo['queryTime']) \
                and str(client['revKey']) == str(revInfo['revKey']):
                    # send client and json
                    client['echoHandler'].write_message(json.dumps(infoDict))
        else:
            return False

    @classmethod
    def sendPublic(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.clients:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

# ---------------------------------------------------
# coroutine task
# ---------------------------------------------------
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop, gen, queues
from datetime import timedelta



class multipleQueryHandler(BaseHandler):
    import probCrawler
    # default crawler object
    query = probCrawler.crawler(queryName='test')


    @gen.coroutine
    def worker(self):
        while not self._q.empty():
            yield self.run()

    @gen.coroutine
    def fetch(self,url):
        # print('fetcing', url)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',}
        response = yield AsyncHTTPClient().fetch(url,headers=headers, raise_error=False,request_timeout=20)
        raise gen.Return(response)


    @gen.coroutine
    def run(self):
        import probCrawler
        try:
            oj,url = yield self._q.get()
            res = yield self.fetch(url)
            html = res.body
            # print oj,type(html)
            if html :
                # deal according to strategy
                # json-format uestc,codeforce,vjudge
                if oj == 'acdream':
                    res = self.query.getAsyncACdream(html)
                if oj == 'uestc':
                    res = self.query.getAsyncUestc(html)
                if oj == 'vjudge':

                    res = self.query.paraseVjudgeJSON(html)

                if oj == 'codeforces':
                    res = self.query.paraseCodeforceJSON(html)

                elif self.query.getOJAuthRule(oj):
                    # get non-JSON format data
                    url,acRegex,submitRegex = self.query.getOJAuthRule(oj)
                    res = self.query.actRegexRules(html,acRegex,submitRegex,oj)

                else :
                    # fail
                    pass
                for oj,ac,submit in res:
                    pass
                    #print oj,ac,submit


        finally:
            self._q.task_done()

    @gen.coroutine
    def genTask(self,name=''):
        self._q = queues.Queue()
        name = self.name
        import probCrawler
        self.name = name

        # traverse non-auth oj rule
        for oj,website,acRegex,submitRegex in self.query.getNoAuthRules():
            success = False
            otherInfo = 0
            # build the URL
            url = website %name
            # put into queue
            yield self._q.put((oj,url))
        # ACDream,Codeforces,vjudge,uestc
        oj = 'uestc'
        url = 'http://acm.uestc.edu.cn/user/userCenterData/%s' %name
        yield self._q.put((oj,url))
        oj = 'acdream'
        url = 'http://acdream.info/user/%s' % name
        yield self._q.put((oj,url))
        oj = 'vjudge'
        url = 'https://cn.vjudge.net/user/solveDetail/%s' %name
        yield self._q.put((oj,url))
        oj = 'codeforces'
        loopFlag = True
        loopTimes = 0
        count = 1000
        startItem = 1+loopTimes*count
        url = 'http://codeforces.com/api/user.status?handle=%s&from=%s' %(name,startItem)
        yield  self._q.put((oj,url))


        for _ in range(100): # open up 100 process
            self.worker()
        # yield self._q.join(timeout=timedelta(seconds=30))

    @tornado.web.asynchronous
    #@tornado.gen.engine
    @tornado.gen.coroutine
    def get(self,*args,**kwargs):
        import probCrawler
        name = self.get_argument("name")
        revKey = self.get_argument('revKey',None)
        timestamp =self.get_argument('timestamp',None)
        self.query = probCrawler.crawler(queryName=name)
        self.name = name
        self.genTask()
        yield self._q.join(timeout=timedelta(seconds=30))

        # ioloop.IOLoop.current().run_sync(self.genTask)
        # prepare the json
        dataDict = {}
        dataDict['ac'] = self.query.acArchive
        #dataDict['ac'] = {}
        tot = 0
        for key, value in self.query.acArchive.items():
            tot += len(value)
            if key:
                try:
                    dataDict['ac'][key] = list(value)
                except Exception as e:
                    logging.error(e)
                    pass
            else:
                pass
        dataDict['submit'] = self.query.submitNum
        dataDict['wrongOJ'] = self.query.wrongOJ
        now = datetime.datetime.now()
        import time
        timestamp = time.mktime(now.timetuple())
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(dataDict))
        self.finish()
        # do databases work
        submitTot = 0
        for oj,submitNum in self.query.submitNum.items():
            submitTot += submitNum
        if submitTot != 0:
            ratio = float(tot)/submitTot
        else:
            ratio = 0.0
        saveData = acRecordArchive(
            name=name,
            pojNum = len(dataDict['ac'].get('poj',[])),
            hduNum = len(dataDict['ac'].get('hdu',[])),
            zojNum = len(dataDict['ac'].get('zoj',[])),
            cfNum = len(dataDict['ac'].get('codeforces',[])),
            acdreamNum = len(dataDict['ac'].get('acdream',[])),

            bzojNum = len(dataDict['ac'].get('hysbz',[])),
            otherOJNum = tot-len(dataDict['ac'].get('poj',[]))
                            -len(dataDict['ac'].get('hdu',[]))
                            -len(dataDict['ac'].get('zoj',[]))
                            -len(dataDict['ac'].get('codeforces',[]))
                            -len(dataDict['ac'].get('acdream',[]))
                            -len(dataDict['ac'].get('hysbz',[])),

            totalNum = tot,
            submitNum = submitTot,
            ratio = ratio,
        )
        saveData.save()
        pass

# -----------------------------------------------------
# feature faq and about
# -----------------------------------------------------

class docRequestHandler(BaseHandler):
    def get(self,pageName,*args,**kwargs):
        if pageName not in ['about','faq','feature','bulk_query_guide']:
            self.write_error(404)
        try:
            self.render('queryProbInfo/%s.html' % (pageName),*args)
        except Exception as e:
            raise e
            self._reason = '瞄~'
            self.write_error(404)

class bulkQueryRequestHandler(BaseHandler):
    import probCrawler
    # default crawler object
    query = probCrawler.crawler(queryName='test')
    # storage all the info about the bulk OJ
    infoDict = {}
    filterOJ = set([])

    @gen.coroutine
    def worker(self):
        while not self._q.empty():
            yield self.run()

    @gen.coroutine
    def fetch(self,url):
        # print('fetcing', url)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',}
        response = yield AsyncHTTPClient().fetch(url,headers=headers, raise_error=False,request_timeout=10)
        raise gen.Return(response)


    @gen.coroutine
    def run(self):
        import probCrawler
        try:
            oj,url,name = yield self._q.get()
            res = yield self.fetch(url)
            html = res.body
            # print oj,type(html)
            if html :
                # deal according to strategy
                # json-format uestc,codeforce,vjudge
                if oj == 'acdream':
                    res = self.query.getAsyncACdream(html)
                if oj == 'uestc':
                    res = self.query.getAsyncUestc(html)
                if oj == 'vjudge':

                    res = self.query.paraseVjudgeJSON(html)

                if oj == 'codeforces':
                    res = self.query.paraseCodeforceJSON(html)

                elif self.query.getOJAuthRule(oj):
                    # get non-JSON format data
                    url,acRegex,submitRegex = self.query.getOJAuthRule(oj)
                    res = self.query.actRegexRules(html,acRegex,submitRegex,oj)

                else :
                    # fail
                    pass
                for oj,ac,submit in res:
                    self.infoDict[name][oj] = (ac,submit)
                    pass
                    # print oj,ac,submit


        finally:
            self._q.task_done()

    @gen.coroutine
    def genTask(self,name=''):

        # name = self.name
        import probCrawler
        self.name = name

        # initialize the dict
        self.infoDict[name] = {}
        # traverse non-auth oj rule
        for oj,website,acRegex,submitRegex in self.query.getNoAuthRules():
            success = False
            otherInfo = 0
            # build the URL
            url = website %name
            # put into queue
            yield self._q.put((oj,url,name))
        # ACDream,Codeforces,vjudge,uestc
        oj = 'uestc'
        url = 'http://acm.uestc.edu.cn/user/userCenterData/%s' %name
        yield self._q.put((oj,url,name))
        oj = 'acdream'
        url = 'http://acdream.info/user/%s' % name
        yield self._q.put((oj,url,name))
        oj = 'vjudge'
        url = 'https://cn.vjudge.net/user/solveDetail/%s' %name
        yield self._q.put((oj,url,name))
        oj = 'codeforces'
        loopFlag = True
        loopTimes = 0
        count = 1000
        startItem = 1+loopTimes*count
        url = 'http://codeforces.com/api/user.status?handle=%s&from=%s' %(name,startItem)
        yield  self._q.put((oj,url,name))

        for _ in range(100): # open up 100 process
            self.worker()



        # yield self._q.join(timeout=timedelta(seconds=30))


    def get(self,*args,**kwargs):
        self.render('queryProbInfo/bulk_query.html')

    @tornado.web.asynchronous
    #@tornado.gen.engine
    @tornado.gen.coroutine

    def post(self,*args,**kwargs):
        # we will use plagiarism system permission
        import probCrawler
        self._q = queues.Queue()
        self.filterOJ = set([])
        self.infoDict = {}
        email = self.get_argument('email')
        self.query = probCrawler.crawler(queryName='')
        accessKey = self.get_argument('accessKey')
        from codePlag.models import filePermitArchive
        # need check right first
        if not filePermitArchive.filter(email=email,isAuth=True,isBanned=False,auth_key=accessKey).exists():
            self._reason = '传递的Email值或者准入密钥有问题/您的Email没有验证成功'
            self._status_code = 500
            self.write_error(500)
            return
        bulkAccount = self.get_argument('namelist')
        # split the text according to lines
        accountList = bulkAccount.split()
        if len(accountList) > 50 :
            self._reason = '批量查询账号超过最大检索数50'
            self._status_code = 500
            self.write_error(500)
        # print(accountList)
        print accountList
        for account in accountList:
            self.genTask(name=account)

        yield self._q.join(timeout=timedelta(seconds=100))
        print self.infoDict
        import tornado.escape
        self.write(tornado.escape.json_encode(self.infoDict))
