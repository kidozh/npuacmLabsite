# -*- coding: UTF-8 -*-
__author__ = 'kidozh'

from core.requestHandler import BaseHandler
from codePlag.codePlagiarism.main import get_sim
from .models import codePlagRecord,fileArchive,filePermitArchive
import os
import cPickle
import uuid
import zipfile
import re

class plagPortalRequestHandler(BaseHandler):
    def get(self,*args,**kwargs):
        self.render('codePlag/index.html')

class docRequestHandler(BaseHandler):
    def get(self,pageName,*args,**kwargs):
        if pageName not in ['privacy','terms_of_service','contact','file_use_guide']:
            self.write_error(404)
            return
        try:
            self.render('codePlag/%s.html' % (pageName),*args)
        except Exception as e:
            raise e
            self._reason = '瞄~'
            self.write_error(404)

class checkerRequestHandler(BaseHandler):
    def get(self,*args,**kwargs):
        self.render('codePlag/single_compare.html')

    def post(self,*args,**kwargs):
        codeA = self.get_argument('codeA')
        codeB = self.get_argument('codeB')
        codeType = self.get_argument('codeType','char')
        if (codeType == 'c/c++'):
            # filter invalid character for windows platform
            import re
            codeA = re.sub('\r','',codeA)
            codeB = re.sub('\r','',codeB)

        A2B,B2A = get_sim(codeA,codeB,language=codeType)

        from .codePlagiarism.winnow import winnow_text_by_default
        from .codePlagiarism.cluster.filter import get_ast_from_c,remove_for_c_parser
        from .codePlagiarism.compare.checkSet import get_common_fingerprint
        # winnowing by text
        if codeType == 'c/c++':
            dealtA = get_ast_from_c(remove_for_c_parser(codeA))
            dealtB = get_ast_from_c(remove_for_c_parser(codeB))
        else:
            dealtA = codeA
            dealtB = codeB
        # winnowing part
        winnowA = winnow_text_by_default(dealtA)
        winnowB = winnow_text_by_default(dealtB)
        unionFingerPrintCnt = get_common_fingerprint(winnowA,winnowB)
        args = locals()
        args.pop('self')
        self.render('codePlag/single_result.html',**args)
        # operating on database
        savedRecord =  codePlagRecord(
            codeA = codeA,
            codeB = codeB,
            similarityA2B = A2B,
            similarityB2A = B2A,
            tokenLenA = len(winnowA),
            tokenLenB = len(winnowB),
            shareTokenLen = unionFingerPrintCnt,
            codeType = codeType,
        )
        savedRecord.save()

class fileCheckerRequestHandler(BaseHandler):
    def get(self,*args,**kwargs):
        self.render('codePlag/uploadFile.html')

    def post(self,*args,**kwargs):
        import uuid
        import zipfile
        email = self.get_argument('email')
        accessKey = self.get_argument('accessKey')
        # need check right first
        if not filePermitArchive.filter(email=email,isAuth=True,isBanned=False,auth_key=accessKey).exists():
            self._reason = '传递的Email值或者准入密钥有问题或者您的Email没有验证成功'
            self.write_error(500)
            return

        self.set_secure_cookie('authEmail',email)
        upload_path=os.path.join(os.path.dirname(__file__),'uploadZipFiles')  #文件的暂存路径
        language = self.get_argument('language','char')
        # print language
        file_metas=self.request.files['file']
        uuidCode = uuid.uuid4()
        # try to create directory
        dirPath =  os.path.join(upload_path,'%s'%(email))
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)


        for meta in file_metas:
            filename=meta['filename']
            # prevent
            filepath=os.path.join(dirPath,'%s_%s'%(uuidCode,filename))
            with open(filepath,'wb') as up:      # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
                # deal with it

        # read zip file
        if not zipfile.is_zipfile(filepath):
            self._reason = '不是合法的ZIP文件'
            self.write_error(500)
            return
        # extract files to extract file
        zipFile = zipfile.ZipFile(filepath, 'r')
        extract_path=os.path.join(os.path.dirname(__file__),'extractZipFiles')
        extractDirPath =  os.path.join(extract_path,'%s'%(email))
        if not os.path.isdir(extractDirPath):
            os.mkdir(extractDirPath)
        extractRoundPath = os.path.join(extractDirPath,'%s_%s'%(uuidCode,filename))
        if not os.path.isdir(extractRoundPath):
            os.mkdir(extractRoundPath)

        zipFile.extractall(extractRoundPath)
        from .codePlagiarism.main import simArray
        simInfo = simArray()
        simInfo.get_simi_from_path(extractRoundPath,language=language)
        # print simInfo.simiMatrix
        args = locals()
        args.pop('self')
        self.render('codePlag/fileResults.html',**args)
        # save to database
        # print filepath
        saveArchive = fileArchive(
            zipFilePath = filepath,
            fileTitle = filename,
            fileUUID = uuidCode,
            issuedEmail = email
        )
        saveArchive.save()

def validateEmail(email):
    if len(email) > 7:
        if re.match("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email) != None:
            return 1
    return 0

# resister handler
class accessUserRegisterRequestHandler(BaseHandler):
    def get(self,*args,**kwargs):
        self.render('codePlag/register_user.html')

    def post(self,*args,**kwargs):
        email = self.get_argument('email')
        if validateEmail(email):
            account,domain = email.split('@')
            # check if domain is correct
            if not( isinstance(domain,str) or isinstance(domain,unicode)):
                #print domain,type(domain)
                self._reason = '域名域不正确'
                self.write_error(500)
                return
            if re.match('^.+edu\.cn$',email) \
                or re.match('^.+rwth-aachen\.de$',email) \
                or re.match('^.+npuacm\.info$',email):
                # this is approved email address
                validEmail = True
                pass
            else:
                validEmail = False

        else:
            self._reason = '邮箱格式不正确'
            self.write_error(500)
            print email
            return
        # do not distinguish email validation in creating account
        # gennerate a random
        # looking for unique
        if filePermitArchive.filter(email=email).exists():
            self._reason = '已经存在同名邮箱'
            self.write_error(500)
            return

        import random
        import string
        AuthKey = ''.join([(string.ascii_letters+string.digits)[x] for x in random.sample(range(0,62),8)])
        newAccount = filePermitArchive(
            email = email,
            auth_key = AuthKey
        )
        newAccount.save()
        # if email pass the validation, then send email
        if validEmail:
            # send email
            from conf.models import configOption
            mailHost = configOption.get(name='mail_host').value
            mailUser = configOption.get(name='mail_user').value
            mailPass = configOption.get(name='mail_pass').value
            mailPort = configOption.get(name='mail_port').value
            # encrypt info
            import json,base64
            infoDict = {'email':email,'auth_key':AuthKey}
            infoString = json.dumps(infoDict)
            encryptString = base64.b64encode(infoString)

            import smtplib
            from email.mime.text import MIMEText
            args = locals()
            args.pop('self')
            html = self.render_string('codePlag/email/register.html',**args)
            msg = MIMEText(html, 'html', 'utf-8')
            msg['Subject'] = '激活您的账户'
            msg['From'] = 'noreply@npuacm.info'
            msg['To'] = email
            smtp_server = mailHost
            from_addr = mailUser
            password = mailPass
            # send email
            server = smtplib.SMTP(smtp_server)
            server.set_debuglevel(1)
            server.starttls()  # use safe mode
            server.login(from_addr, password)
            server.sendmail(from_addr, email, msg.as_string())
            server.quit()
        args = locals()
        args.pop('self')
        self.render('codePlag/register_result.html',**args)

class jplagCheckerRequestHandler(BaseHandler):
    # execute order

    def get(self,*args,**kwargs):
        self.render('codePlag/jplag_file_upload.html')

    def post(self,*args,**kwargs):
        email = self.get_argument('email')
        accessKey = self.get_argument('accessKey')
        # need check right first
        if not filePermitArchive.filter(email=email,isAuth=True,isBanned=False,auth_key=accessKey).exists():
            print filePermitArchive.filter(email=email,isAuth=True,isBanned=False,auth_key=accessKey).exists()
            self._reason = '传递的Email值或者准入密钥有问题或者您的Email没有验证成功'
            self._status_code = 500
            self.write_error(500)
            return


        self.set_secure_cookie('authEmail',email)
        upload_path=os.path.join(os.path.dirname(__file__),'uploadZipFiles')  #文件的暂存路径
        language = self.get_argument('language','c/c++')
        if not language in ['java17', 'java15', 'java15dm', 'java12', 'java11', 'c/c++', 'c#-1.2', 'char', 'text', 'scheme']:
            self._reason = '错误的文件描述形式'
            self.write_error(500)
            return
        # print language
        file_metas=self.request.files['file']
        uuidCode = uuid.uuid4()
        # try to create directory
        dirPath =  os.path.join(upload_path,'%s'%(email))
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)

        if len(file_metas) != 1:
            self._reason = '文件上传不正确。'
            self.write_error(500)
            return



        for meta in file_metas:
            filename=meta['filename']
            # prevent

            filepath=os.path.join(dirPath,'%s_%s'%(uuidCode,filename))
            # get file name
            if not re.match('\w*\.zip',filename) :
                pass
                self._reason = '错误的文件名'
                self.write_error(500)
                return
            # get size
            if len(meta['body']) > 10 * 1024 * 1024:
                self._reason = '请上传小于10MB的ZIP文件'
                self.write_error(500)
                return

            # get Content-Type
            validContentType = ['application/zip', 'application/octet-stream','application/x-zip-compressed']
            if meta['content_type'] not in validContentType:
                self._reason = '文件类型不正确'
                self.write_error(500)
                return

            with open(filepath,'wb') as up:      # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
                # deal with it
        # think if filename is correct


        # read zip file
        if not zipfile.is_zipfile(filepath):
            self._reason = '不是合法的ZIP文件'
            self.write_error(500)
            self.finish()
            return

        # extract files to extract file
        zipFile = zipfile.ZipFile(filepath, 'r')
        extract_path=os.path.join(os.path.dirname(__file__),'extractZipFiles')
        extractDirPath =  os.path.join(extract_path,'%s'%(email))
        if not os.path.isdir(extractDirPath):
            os.mkdir(extractDirPath)
        extractRoundPath = os.path.join(extractDirPath,'%s_%s'%(uuidCode,filename))
        if not os.path.isdir(extractRoundPath):
            os.mkdir(extractRoundPath)

        zipFile.extractall(extractRoundPath)
        # directly use JPLAG

        # traverse all the contest directory
        contestDir = []
        # save for title
        contestIndex = []
        for root,adir,file in os.walk(extractRoundPath):
            contestIndex = adir

            break
        for prob in contestIndex:
            contestDir.append(os.path.join(extractRoundPath,prob))
        # execute jplag
        import subprocess
        resultDir = os.path.join(os.path.dirname(__file__),'result')
        # try to create directory for result
        userResultDir =  os.path.join(resultDir,'%s'%(email))
        if not os.path.isdir(userResultDir):
            os.mkdir(userResultDir)
        contestResultDir = os.path.join(userResultDir,'%s_%s'%(uuidCode,filename))
        if not os.path.isdir(contestResultDir):
            os.mkdir(contestResultDir)

        for index,contestDir in enumerate(contestDir):
            eachProbResultDir = os.path.join(contestResultDir,contestIndex[index])
            command = 'java -jar codePlag/Jplag.jar -vq -l %s -s %s -r %s'%(language,contestDir,eachProbResultDir)
            a = subprocess.Popen(command, shell=True)
            a.wait()
            # execure by order

        # check the files
        from bs4 import BeautifulSoup
        praseDictInfo = dict()
        for index,prob in enumerate(contestIndex):
            praseDictInfo[prob] = {}
            # get problems title and its result
            eachProbResultDir = os.path.join(contestResultDir,contestIndex[index])
            # parse JPLAG files
            indexFilePath = os.path.join(eachProbResultDir,'index.html')
            with open(indexFilePath,'r') as indexFile :
                indexContent = indexFile.read()
                indexsoup = BeautifulSoup(indexContent,'lxml')
                summaryInfo,praseInfo,averageInfo,maxInfo  = indexsoup.find_all('table')

            # first get summary info
            validSubmission = summaryInfo.find_all('tr')[2].find_all('code')[0].string
            praseDictInfo[prob]['validSubmission'] = validSubmission
            praseDictInfo[prob]['simiRatio'] = {}
            for eachMatchRow in maxInfo.find_all('tr'):
                orignNode = eachMatchRow.find_all('td')[0]
                probDOM = eachMatchRow.find_all('td')[2:]
                orignText = orignNode.string
                praseDictInfo[prob]['simiRatio'][orignText] = []
                for compareNode in probDOM:
                    compareCode = compareNode.a.string
                    ratio = compareNode.font.string
                    praseDictInfo[prob]['simiRatio'][orignText].append((compareCode,ratio))



            # get MAX average Info


        args = locals()
        args.pop('self')
        self.render('codePlag/jplag_result_index.html',**args)
        # handle the database data
        import json
        archive = fileArchive(
            zipFilePath = filepath,
            extractFilePath = extractRoundPath,
            resultFilePath = contestResultDir,
            storageInfo = json.dumps(praseDictInfo),
            fileTitle = filename,
            fileUUID = uuidCode,
            issuedEmail = email,
            codeType = language
        )
        archive.save()


class exportJplagData(BaseHandler):
    def get(self,uuid,filename,*args,**kwargs):
        import os
        email = self.get_secure_cookie('authEmail')
        # need auth its priority
        archive = fileArchive.filter(issuedEmail =email,fileTitle=filename,fileUUID=uuid)
        if archive.count() == 1:
            # ensure there is only one
            topArchive = archive[0]
            resultFilePath = topArchive.resultFilePath
            filelist = []
            dirname = resultFilePath
            if os.path.isfile(dirname):
                filelist.append(dirname)
            else :
                for root, dirs, files in os.walk(dirname):
                    for name in files:
                        filelist.append(os.path.join(root, name))
            # append filelist
            zipFileName = 'Result_%s@%s' %(topArchive.fileUUID,filename)
            self.set_header ('Content-Type', 'application/octet-stream')
            self.set_header ('Content-Disposition', 'attachment; filename=%s' %(zipFileName))
            # give buf_size per sec
            buf_size = 4096
            savedFilePath = 'codePlag/resultZip/%s'%(zipFileName)
            with zipfile.ZipFile(savedFilePath,'w',zipfile.zlib.DEFLATED) as zf:
                # print zipFileName
                for tar in filelist:
                    linkComma = ''
                    if os.environ.get('OS') == 'Windows_NT':
                        linkComma = '\\'
                        arcList = tar.split('\\')[-2:]
                    else:
                        linkComma = '/'
                        arcList = tar.split('/')[-2:]

                    arcName = ''
                    for i,name in enumerate(arcList):
                        if i != 0:
                            arcName += linkComma
                        arcName += name
                    zf.write(tar,arcname=arcName)

            with open(savedFilePath, 'rb') as f:
                while True:
                    data = f.read(buf_size)
                    if not data:
                        break
                    self.write(data)

            # self.write('1')
            self.finish()

class authRequestHandler(BaseHandler):
    def get(self,authString,*args,**kwargs):
        import base64
        import json
        auth = False
        encryptJsonString = base64.b64decode(authString)
        encryptDict = json.loads(encryptJsonString)
        email = encryptDict.get('email',None)
        auth_key = encryptDict.get('auth_key',None)
        if filePermitArchive.filter(email=email,auth_key=auth_key):
            activateAccount = filePermitArchive.get(email=email,auth_key=auth_key)
            if activateAccount.isAuth:
                reason = '账户已经被激活，无需重新激活'
            else:
                activateAccount.isAuth = True
                activateAccount.save()
                reason = '成功激活该账户'
                auth = True
        else:
            reason = '无效'
        args = locals()
        args.pop('self')
        self.render('codePlag/activate_result.html',**args)

class fileArchiveQueryRequestHandler(BaseHandler):
    def get(self,*args,**kwargs):
        import time
        email = self.get_secure_cookie('authEmail')
        page = self.get_argument('page')
        pageSize = self.get_argument('pageSize',20)
        draw = self.get_argument('draw')
        # page size default value is 10
        pageSize = 10
        fileArchiveRow = fileArchive.filter(issuedEmail=email).\
            order_by(fileArchive.submit_time.desc()).paginate(int(page), int(pageSize))
        retDict = {}
        retDict['draw'] = draw
        retDict['email'] = email
        retDict['recordsLength'] = fileArchiveRow.count()
        retDict['recordsTotal'] = fileArchive.filter(issuedEmail=email).count()
        retDict['data'] = []
        for query in fileArchiveRow:
            infoDict = {}
            infoDict['uuid'] = query.fileUUID
            infoDict['codeType'] = query.codeType
            infoDict['filename'] = query.fileTitle
            infoDict['id'] = query.id
            infoDict['downloadUrl'] = self.reverse_url('codePlag.view.exportJplagData',query.fileUUID,query.fileTitle)
            infoDict['submitTime'] = time.mktime(query.submit_time.timetuple())
            retDict['data'].append(infoDict)
        import tornado.escape
        self.write(tornado.escape.json_encode(retDict))
        self.finish()






