# -*- coding: UTF-8 -*-
__author__ = 'kidozh'


import urllib2
import cookielib
import re
import json
import urllib

class crawler:
    '''
    This is the main crawler which contains a dictionary.
    This dictionary's key is the judge name,value is a set that contains each problem that user has ACed.
    As for submit condition , just store the number.
    '''
    name = ''
    acArchive ={}
    submitNum = {}
    # OJ's name : [user,user]
    wrongOJ = {}
    # match dictionary.dict[oj]:[acRegex],[submitRegex]
    matchDict = {}
    supportedOJ = ['poj','hdu','zoj','codeforces','fzu','acdream','bzoj','ural','csu','hust','spoj','sgu','vjudge','bnu','cqu','uestc']
    def __init__(self,queryName=''):
        '''
        This is the initial part which describe the crawler opener.
        '''
        self.headers = {
            'Accept-Language':'zh_CN-CN,zh_CN;q=0.8',
            'Connection':'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.name = queryName
        '''
        initialize all the data structure
        '''
        for oj in self.supportedOJ:
            # for achive ,use set
            self.submitNum[oj] = 0
            self.acArchive[oj] = set([])
            # for problem , use list
            self.wrongOJ[oj]=[]

        '''
        read the dictionary which guide spider to browser website and how to match information
        '''
        matchDict = {}
        matchDict['poj'] = {}

    def getNoAuthRules(self):
        import ConfigParser
        import os
        cf = ConfigParser.ConfigParser()
        configFilePath = os.path.join(os.path.dirname(__file__), "regexDict.ini")
        cf.read(configFilePath)
        # travel all the useable site
        return [(oj,cf.get(oj,'website'),cf.get(oj,'acRegex'),cf.get(oj,'submitRegex')) for oj in cf.sections()]

    def getOJAuthRule(self,ojName):
        '''
        return corresponding rule
        :param ojName:
        :return:
        '''
        import ConfigParser
        import os
        cf = ConfigParser.ConfigParser()
        configFilePath = os.path.join(os.path.dirname(__file__), "regexDict.ini")
        cf.read(configFilePath)
        for oj in cf.sections():
            if oj == ojName:
                return cf.get(oj,'website'),cf.get(oj,'acRegex'),cf.get(oj,'submitRegex')
        return None

    def actRegexRules(self,html,acRegex,submitRegex,oj):
        submission = re.findall(submitRegex, html, re.S)
        acProblem = re.findall(acRegex, html, re.S)
        #print '# submission : ', submission
        #print '# problem : ', acProblem
        # for submit
        try:
            self.submitNum[oj] += int(submission[0])
            yield oj, len(set(acProblem)), submission[0]
        except:
            self.wrongOJ[oj].append(self.name)
            yield oj,0,0
        # for AC merge all the information
        if type(self.acArchive[oj]) == list:
            self.acArchive[oj] = set(self.acArchive[oj]) | set(acProblem)
        else:
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)



    def followRules(self,oj,website,acRegex,submitRegex):
        name = self.name
        req = urllib2.Request(
            url=website % name,
            headers=self.headers
        )
        try:
            html = self.opener.open(req).read(timeout=5)
        except:
            self.wrongOJ[oj].append(name)
            return 0
        submission = re.findall(submitRegex, html, re.S)
        acProblem = re.findall(acRegex, html, re.S)
        print '# submission : ', submission
        print '# problem : ', acProblem
        # for submit
        try:
            self.submitNum[oj] += int(submission[0])
        except:
            self.wrongOJ[oj] = name
            return 0
        # for AC merge all the information
        self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
        return html

    def getInfoNoAuth(self,queryName='kidozh'):
        '''
        This function only browser the website without authentication and also use regex.
        For 'poj','hdu','zoj','fzu','acdream','bzoj','ural','csu','hust','spoj','sgu','vjudge','bnu','cqu','uestc'
        :param query: queryName
        :return:
        '''
        import ConfigParser
        import os
        if queryName == '':
            name = self.name
        else:
            name = queryName
        cf = ConfigParser.ConfigParser()
        configFilePath = os.path.join(os.path.dirname(__file__), "regexDict.ini")
        cf.read(configFilePath)
        # travel all the useable site
        for oj in cf.sections():
            website = cf.get(oj,'website')
            acRegex = cf.get(oj,'acRegex')
            submitRegex = cf.get(oj,'submitRegex')
            print website %name
            req = urllib2.Request(
                url=website %name,
                headers=self.headers
            )
            try:
                html = self.opener.open(req).read()
            except:
                self.wrongOJ[oj].append(name)
                continue
            submission = re.findall(submitRegex, html, re.S)
            acProblem = re.findall(acRegex, html, re.S)
            print '# submission : ',submission
            print '# problem : ',acProblem
            # for submit
            try:
                self.submitNum[oj]+=int(submission[0])
            except:
                self.wrongOJ[oj] = name
                continue
            # for AC merge all the information
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
            #print submission[0],acProblem
            #return submission[0], acProblem

    def getACdream(self,queryName=''):
        oj = 'acdream'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://acdream.info/user/' + name,
            headers=self.headers
        )
        html = ''
        try:
            html = self.opener.open(req).read()
        except:
            self.wrongOJ[oj].append(name)
            return 0
        submission = re.findall('Submissions: <a href="/status\?name=.*?">([0-9]*?)</a>', html, re.S)
        linkAddress = re.findall(
            r'List of <span class="success-text">solved</span> problems</div>(.*?)<div class="block block-warning">',
            html, re.S)
        try:
            acProblem = re.findall(r'<a class="pid" href="/problem\?pid=[0-9]*?">([0-9]*?)</a>', linkAddress[0], re.S)
            self.submitNum[oj] += int(submission[0])
        except:
            self.wrongOJ[oj].append(name)
            return 0
        self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
        return submission[0],acProblem

    def getAsyncACdream(self,html,queryName=''):
        oj = 'acdream'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        submission = re.findall('Submissions: <a href="/status\?name=.*?">([0-9]*?)</a>', html, re.S)
        linkAddress = re.findall(
            r'List of <span class="success-text">solved</span> problems</div>(.*?)<div class="block block-warning">',
            html, re.S)
        try:
            acProblem = re.findall(r'<a class="pid" href="/problem\?pid=[0-9]*?">([0-9]*?)</a>', linkAddress[0], re.S)
            self.submitNum[oj] += int(submission[0])
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
            yield oj, len(acProblem),submission[0]
        except:
            self.wrongOJ[oj].append(name)
            yield oj,0,0



    def showsgu(self, queryName=''):
        oj = 'sgu'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        postData = {
            'find_id': name
        }
        postData = urllib.urlencode(postData)
        req = urllib2.Request(
            url='http://acm.sgu.ru/find.php',
            headers=self.headers,
            data=postData
        )
        html = ''
        try:
            html = self.opener.open(req, timeout=5).read()
        except:
            self.wrongOJ[oj].append(name)
            return 0
        sem = re.findall(r'</h5><ul><li>[0-9]*?.*?<a href=.teaminfo.php.id=([0-9]*?).>.*?</a></ul>', html, re.S)
        # print sem
        try:
            temp = sem[0]
            req = urllib2.Request(
                url='http://acm.sgu.ru/teaminfo.php?id=' + str(temp),
                headers=self.headers
            )
            result = self.opener.open(req, timeout=10)
            html = result.read()
            submission = re.findall(r'Submitted: ([0-9]*?)', html, re.S)
            acProblem = re.findall(r'<font color=.*?>([0-9]*?)&#160</font>', html, re.S)
            # get all the information
            self.submitNum[oj]+=int(submission[0])
            self.acArchive[oj] = self.acArchive[oj]|set(acProblem)
            return submission[0],acProblem
        except:
            self.wrongOJ[oj].append(name)
            return 0



    def getcodeforces(self,queryName=''):
        '''
        get JSON information from codeforces API and parser it
        :param queryName:
        :return: Boolean value which indicates success
        '''
        oj = 'codeforces'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        loopFlag = True
        loopTimes = 0
        count = 1000
        startItem = 1+loopTimes*count
        endItem = (loopTimes+1)*count
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
                jsonString = urllib2.urlopen(website).read()
            except:
                self.wrongOJ[oj].append(name)
                return 0
            import json
            data = json.loads(jsonString)
            if data[u'status'] == u'OK':
                if len(data[u'result']) == 0:
                    break
                else:
                    pass
                # store the submit number
                self.submitNum[oj] += len(data[u'result'])

                # print self.subcf
                for i in data[u'result']:
                    # only accept AC problem
                    if i[u'verdict'] == 'OK':
                        problemInfo = i[u'problem']
                        problemText ='%s%s' %(problemInfo[u'contestId'],problemInfo[u'index'])
                        self.acArchive[oj].add(problemText)
            else:
                break
        return True

    def asyncGetCodeforces(self,queryName=''):
        '''
        get JSON information from codeforces API and parser it
        :param queryName:
        :return: Boolean value which indicates success
        '''
        import tornado.httpclient
        import tornado.gen
        oj = 'codeforces'
        print 'start CodeForce'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        loopFlag = True
        loopTimes = 0
        count = 1000
        startItem = 1+loopTimes*count
        endItem = (loopTimes+1)*count
        # init async part
        client = tornado.httpclient.AsyncHTTPClient()

        # loop start
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
                req = tornado.httpclient.HTTPRequest(website,headers=self.headers,request_timeout=5)
                #jsonString = urllib2.urlopen(website).read()
                response =  yield tornado.gen.Task(client.fetch,req)
                if response.code == 200:
                    jsonString = response.body
                else:
                    # raise a exception
                    raise BaseException
            except:
                self.wrongOJ[oj].append(name)
                return
            import json
            data = json.loads(jsonString)
            if data[u'status'] == u'OK':
                if len(data[u'result']) == 0:
                    break
                else:
                    pass
                # store the submit number
                self.submitNum[oj] += len(data[u'result'])

                # print self.subcf
                for i in data[u'result']:
                    # only accept AC problem
                    if i[u'verdict'] == 'OK':
                        problemInfo = i[u'problem']
                        problemText ='%s%s' %(problemInfo[u'contestId'],problemInfo[u'index'])
                        self.acArchive[oj].add(problemText)
            else:
                break


    def getSpoj(self, queryName=''):
        oj = 'spoj'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://www.spoj.com/users/%s'% name,
            headers=self.headers
        )
        html = ''
        try:
            html = self.opener.open(req).read()
        except:
            self.wrongOJ[oj].append(name)
            return 0
        submission = re.findall(r'Solutions submitted</dt>.*?<dd>([0-9]*?)</dd>', html, re.S)
        rawinfo = re.findall(r'<table class="table table-condensed">(.*?)</table>', html, re.S)
        try:
            acProblem = re.findall(r'<a href="/status/.*?/">(.*?)</a>', rawinfo[0], re.S)
            self.submitNum[oj]+=int(submission[0])
            self.acArchive[oj]=self.acArchive[oj]|set(acProblem)
        except:
            self.wrongOJ[oj].append(name)
            return 0
        return submission[0],acProblem

    def getVjudge(self,queryName=''):
        '''
        We will set up a cache pool to restore the cookie and keep it
        :param queryName:
        :return:
        '''
        import tornado.httpclient
        import tornado.gen
        oj = 'vjudge'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        client = tornado.httpclient.AsyncHTTPClient()
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
        loginReq = urllib2.Request(
            url='http://vjudge.net/user/login',
            data=urllib.urlencode(publicAccountDict),
            headers=VJheaders
        )
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        try:
            # hold the cookie
            response = opener.open(loginReq, timeout=5)
        except Exception as e:
            self.wrongOJ[oj] = name
            return
        # query the API
        loopFlag = True
        maxId = None
        pageSize=100
        status=None
        while loopFlag:
            req = urllib2.Request(
                url='http://vjudge.net/user/submissions?username=%s&pageSize=%s&status=%s&maxId=%s' % (name, pageSize, status, maxId),
                headers=VJheaders
            )
            try:
                jsonString = opener.open(req).read()
                dataDict = json.loads(jsonString)
                dataList = dataDict['data']
            except Exception as e:
                self.wrongOJ[oj].append(name)
                break
            for vID, orignID, ojName, probID, result, execSeconds, execMemory, languages, codeLength, submitTime in dataList:
                oj = ojName.lower()
                # only extract AC status
                if result == 'AC':
                    if self.acArchive.has_key(oj) :
                        self.acArchive[oj].add(probID)
                    else:
                        # initialize the dict, insert value set
                        self.acArchive[oj] = set().add(probID)
                else:
                    pass
                self.submitNum[oj] += 1
                # vjudge's submit is not added to total number
                self.submitNum['vjudge']+=1
        return 1

    def asyncGetVjudge(self,queryName=''):
        '''
        We will set up a cache pool to restore the cookie and keep it
        tornado will use it
        :param queryName:
        :return:
        '''
        import tornado.httpclient
        import tornado.gen
        oj = 'vjudge'
        if queryName == '':
            name = self.name
        else:
            name = queryName
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
        website = 'http://vjudge.net/user/login'
        # init non-block part
        client = tornado.httpclient.AsyncHTTPClient()
        # auth
        authData = urllib.urlencode(publicAccountDict)
        req = tornado.httpclient.HTTPRequest(website,headers=self.headers,request_timeout=5,method='POST',body=authData)

        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        # client fetch the data
        print 'yes'
        response =  yield tornado.gen.Task(client.fetch,req)
        #response = client.fetch(req)
        if response.code == 200:
            # auth successfully
            print response
            pass
        else:
            print response
            self.wrongOJ[oj] = name
            return
        # query the API
        loopFlag = True
        maxId = None
        pageSize=100
        status=None
        while loopFlag:
            req = urllib2.Request(
                url='http://vjudge.net/user/submissions?username=%s&pageSize=%s&status=%s&maxId=%s' % (name, pageSize, status, maxId),
                headers=VJheaders
            )
            try:
                jsonString = opener.open(req).read()
                dataDict = json.loads(jsonString)
                dataList = dataDict['data']
            except Exception as e:
                self.wrongOJ[oj].append(name)
                break
            for vID, orignID, ojName, probID, result, execSeconds, execMemory, languages, codeLength, submitTime in dataList:
                oj = ojName.lower()
                # only extract AC status
                if result == 'AC':
                    if self.acArchive.has_key(oj):
                        self.acArchive[oj].add(probID)
                    else:
                        # initialize the dict, insert value set
                        self.acArchive[oj] = set().add(probID)
                else:
                    pass
                self.submitNum[oj] += 1
                # vjudge's submit is not added to total number
                self.submitNum['vjudge']+=1
        return

    def getUestc(self,queryName=''):
        oj = 'uestc'
        if queryName == '':
            name = self.name
        else:
            name = queryName
        req = urllib2.Request(
            url='http://acm.uestc.edu.cn/user/userCenterData/%s' % name,
            headers=self.headers,
        )
        try:
            jsonString = self.opener.open(req).read()
        except:
            self.wrongOJ[oj].append(name)
            return 0
        dataDict = json.loads(jsonString)
        # detect AC item
        if dataDict['result'] == 'error':
            self.wrongOJ[oj].append(name)
            return 0
        else:
            for dictItem in dataDict['problemStatus']:
                if dictItem['status'] == 1:
                    self.acArchive[oj].add(dictItem['problemId'])
                else:
                    pass
            self.submitNum[oj] += len(dataDict['problemStatus'])
        return 1

    def getAsyncUestc(self,jsonString):
        oj = 'uestc'
        name = self.name
        dataDict = json.loads(jsonString)
        # detect AC item
        if dataDict['result'] == 'error':
            self.wrongOJ[oj].append(name)
            yield oj,0,0
        else:
            ac = 0
            for dictItem in dataDict['problemStatus']:
                if dictItem['status'] == 1:
                    self.acArchive[oj].add(dictItem['problemId'])
                    ac += 1
                else:
                    pass
            self.submitNum[oj] += len(dataDict['problemStatus'])
            yield oj,ac,len(dataDict['problemStatus'])

    def paraseCodeforceJSON(self,html):
        oj = 'codeforces'
        try:
            data = json.loads(html)
        except:
            yield 0,0,0
            return

        submit = 0
        ac = 0
        if data[u'status'] == u'OK':
            if len(data[u'result']) == 0:
                yield oj,0,0
            else:
                pass
            # store the submit number
            self.submitNum[oj] += len(data[u'result'])
            submit += len(data[u'result'])
            for i in data[u'result']:
                # only accept AC problem
                if i[u'verdict'] == 'OK':
                    problemInfo = i[u'problem']
                    problemText ='%s%s' %(problemInfo[u'contestId'],problemInfo[u'index'])
                    # append set
                    if type(self.acArchive[oj]) == list:
                        self.acArchive[oj] = set(self.acArchive[oj])
                    self.acArchive[oj].add(problemText)
                    ac += 1
                else:
                    pass
        yield oj,ac,submit

    def paraseVjudgeJSON(self,jsonString):
        oj = 'vjudge'
        name = self.name
        try:
            dataDict = json.loads(jsonString)
        except:
            yield oj,0,0
            return
        # detect AC item
        acRecord = dataDict['acRecords']
        submitRecord = dataDict['failRecords']

        ac = 0
        submit = 0
        # record ac val
        for oj,acProbList in acRecord.items():
            if submitRecord.has_key(oj):
                submitR = len(submitRecord[oj])
            else:
                submitR = 0
            ojAC = len(acRecord[oj]) + submitR
            oj = oj.lower()
            if self.submitNum.has_key(oj):
                self.submitNum[oj] += ojAC
            else:
                self.submitNum[oj] = ojAC
            ac +=len(acProbList)
            submit += len(acProbList)
            if self.acArchive.has_key(oj) :
                if type(self.acArchive[oj]) == list:
                    self.acArchive[oj] = set(self.acArchive[oj])
                self.acArchive[oj] |= set(acProbList)

            else:
                # renew the set()
                self.acArchive[oj] = set(acProbList)

        # record submit value
        for oj,submitProbList in submitRecord.items():
            submit += len(submitProbList)
        yield oj,ac,submit


    def getTotalACNum(self):
        '''
        get the total number from dictionary that store the AC data.
        :return: the total AC's
        '''
        totalNum = 0
        for key,value in self.acArchive.items():
            # value should be a set
            totalNum += len(value)
        return totalNum

    def getTotalSubmitNum(self):
        '''
        get the total number from dictionary that store the submit data
        :return:
        '''
        totalNum = 0
        for key,value in self.submitNum.items():
            if key != 'vjudge':
                totalNum += int(value)
            else:
                # discard the submission data about vjudge
                pass
        return totalNum

    def changeCurrentName(self,name):
        self.name = name
        return True



if __name__ == '__main__':
    a = crawler(queryName='kidozh')
    print a.asyncGetVjudge()

    '''print a.getNoAuthRules()
    a.getInfoNoAuth()
    a.getACdream()
    a.getcodeforces()
    a.getSpoj()
    a.getUestc()
    a.getVjudge()
    print a.acArchive
    print a.submitNum
    '''