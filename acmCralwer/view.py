# coding=utf-8
__author__ = 'exbot'
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.websocket
import datetime
import urllib2
import json
import logging
import time

class queryIndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('queryProblem/index.html',error=False)

    def isNameValid(self,queryName):
        '''
        just a regex function to detect whether queryName is correct.
        :param queryName: name that waiting for detect
        :return: boolean value whether name is valid or not.
        '''
        import re
        return re.match(r'^\w*$',queryName)

    def post(self, *args, **kwargs):
        '''
        just a rendering page
        :param args:
        :param kwargs:
        :return: none
        '''
        mainName = self.get_argument("mainName")
        viceName = self.get_argument("viceName",'')
        # use regex to fill the match the name
        if self.isNameValid(mainName) and self.isNameValid(viceName):
            # this name is valid...
            self.render('queryProblem/query.html',mainName=mainName,viceName=viceName)
        else:
            self.render('queryProblem/error.html',error=True)


class queryInfoHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@tornado.gen.engine
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        mainName = self.get_argument("mainName")
        revKey = self.get_argument('revKey')
        timestamp =self.get_argument('timestamp')
        # for websocket auth
        self.timestamp = timestamp
        self.revKey = revKey
        self.mainName = mainName
        if self.isNameValid(mainName):
            import cralwer
            import json
            import time
            name = mainName
            query = cralwer.crawler(queryName=mainName)
            client = tornado.httpclient.AsyncHTTPClient()
            # non-block part
            cnt = 0
            for oj,website,acRegex,submitRegex in query.getNoAuthRules():
                # non-block for each OJ
                t0 = time.time()
                cnt +=1
                url = website %mainName
                req = tornado.httpclient.HTTPRequest(url,headers=query.headers,request_timeout=5)
                response =  yield tornado.gen.Task(client.fetch,req)
                if response.code == 200:
                    otherInfo = time.time()-t0
                    res = query.actRegexRules(response.body,acRegex,submitRegex,oj)
                    for oj,ac,submit in res:
                        self.sendRealTimeInfo(oj,name,ac,submit,otherInfo)
                else:
                    pass

            # uestc
            acdreamURL = 'http://acm.uestc.edu.cn/user/userCenterData/%s' %mainName
            t0 = time.time()
            response = yield tornado.gen.Task(client.fetch,acdreamURL,headers=query.headers)
            if response.code == 200:
                otherInfo = time.time()-t0
                res = query.getAsyncUestc(response.body)
                for oj,ac,submit in res:
                    self.sendRealTimeInfo(oj,name,ac,submit,otherInfo)
            else:
                pass

            t0 = time.time()
            acdreamURL = 'http://acdream.info/user/%s' % mainName
            response = yield tornado.gen.Task(client.fetch, acdreamURL, headers=query.headers)
            if response.code == 200:
                otherInfo = time.time()-t0
                res = query.getAsyncACdream(response.body)

                for oj,ac,submit in res:
                    self.sendRealTimeInfo(oj,name,ac,submit,otherInfo)

            else:
                pass
            # codeforces
            oj = 'codeforces'
            query.acArchive[oj] = set()
            loopFlag = True
            loopTimes = 0
            count = 1000
            startItem = 1+loopTimes*count
            endItem = (loopTimes+1)*count
            name = mainName
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
                    else:
                        # raise a exception
                        raise BaseException
                except:
                    query.wrongOJ[oj].append(name)
                    break
                import json
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
            otherInfo = time.time()-t0
            self.sendRealTimeInfo(oj,name,ac,submit,otherInfo)
            # vjudge async part
            query.acArchive['vjudge'] = set()
            VJheaders = {
                'Host': 'vjudge.net',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'deflate',
                # 'Cookie':'ga=GA1.3.1416134436.1469179876',
            }
            publicAccountDict = {
                'username': '2013300116',
                'password': '8520967123'
            }
            import urllib
            website = 'http://vjudge.net/user/login'
            authData = urllib.urlencode(publicAccountDict)
            req = tornado.httpclient.HTTPRequest(website,headers=VJheaders,request_timeout=5,method='POST',body=authData)
            # set clock time
            t0 = time.time()

            response =  yield tornado.gen.Task(client.fetch,req)
            #response = client.fetch(req)
            if response.code == 200:
                # auth successfully
                cookieHeaders = response.headers
                VJheaders['Cookie'] = cookieHeaders['set-Cookie']
            else:
                query.wrongOJ[oj] = name
            # query the API
            loopFlag = True
            maxId = ''
            pageSize=100
            status=''
            ac = 0
            submit = 0
            while loopFlag:
                website = 'http://vjudge.net/user/submissions?username=%s&pageSize=%s&status=%s&maxId=%s' % (name, pageSize, status, maxId)
                req = tornado.httpclient.HTTPRequest(website,headers=VJheaders,request_timeout=5)
                response =  yield tornado.gen.Task(client.fetch,req)
                #response = client.fetch(req)
                if response.code == 200:
                    # auth successfully
                    jsonString = response.body
                    dataDict = json.loads(jsonString)
                    try:
                        dataList = dataDict['data']
                    except:
                        query.wrongOJ[oj] = name
                        break
                else:
                    query.wrongOJ[oj] = name
                    break
                if len(dataList) <= 1:
                    break
                else:
                    pass
                for vID, orignID, ojName, probID, result, execSeconds, execMemory, languages, codeLength, submitTime in dataList:
                    oj = ojName.lower()
                    # only extract AC status
                    if result == 'AC':
                        ac +=1
                        if query.acArchive.has_key(oj) and isinstance(query.acArchive[oj],set):
                            query.acArchive[oj].add(probID)
                            try:
                                query.acArchive['vjudge'].add( '%s %s' %(oj,probID) )
                            except:
                                try:
                                    query.acArchive['vjudge'] = set(query.acArchive['vjudge'])
                                    query.acArchive['vjudge'].add('%s %s' %(oj,probID))
                                except:
                                    pass
                                pass
                        else:
                            # initialize the dict, insert value set
                            query.acArchive[oj] = set()
                            query.acArchive[oj].add('%s %s' %(oj,probID))
                            if isinstance(query.acArchive['vjudge'],list):
                                query.acArchive['vjudge'] = set(query.acArchive['vjudge'])
                            else:
                                pass
                            query.acArchive['vjudge'].add('%s %s' %(oj,probID) )
                    else:
                        pass
                    if query.submitNum.has_key(oj):
                        query.submitNum[oj] += 1
                    else:
                        # initialize the dict, insert value
                        query.submitNum[oj] = 1

                    # vjudge's submit is not added to total number
                    query.submitNum['vjudge']+=1
                    submit +=1
                maxId = dataList[-1][0]
        else:
            raise tornado.web.HTTPError(500,log_message='Invalid name')
        otherInfo = time.time()-t0
        oj = 'vjudge'
        self.sendRealTimeInfo(oj,name,ac,submit,otherInfo)

        # prepare the json
        dataDict = {}
        dataDict['ac'] = query.acArchive
        #dataDict['ac'] = {}
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
        now = datetime.datetime.now()
        import time
        timestamp = time.mktime(now.timetuple())
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(dataDict))
        #self.finish(dataDict)
        self.finish()


    def isNameValid(self, queryName):
        '''
        just a regex function to detect whether queryName is correct.
        :param queryName: name that waiting for detect
        :return: boolean value whether name is valid or not.
        '''
        import re
        return re.match(r'^\w*$', queryName)

    def sendRealTimeInfo(self,oj,name,ac,submit,otherInfo):
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
            'ac':ac,
            'submit':submit,
            'name':name,
            'extra':otherInfo,
            'queryTime':queryTime,
        }
        try:
            echoProblemHandler.sendInfo(revInfo,infoDict)
            return  True
        except Exception as e:
            logging.error('Sending websocket is fail')
            return False


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

