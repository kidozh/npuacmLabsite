__author__ = 'kidozh'
# -*- coding: UTF-8 -*-

from importlib import import_module
from core.exceptions import ImproperlyConfigured

class urlPackage:
    """
    store the URL
    """
    pattern = []
    # this is the map from handler to URL
    URLMapper = {}
    def __init__(self,url_module):
        # check whether this file is properly configured
        if isinstance(url_module,str):
            # url_module is string , just import it
            urlconf_module = import_module(url_module)
        patterns = getattr(urlconf_module, 'urlpatterns', [])
        # get this
        if isinstance(patterns,list):
            self.patterns = patterns
        else:
            raise ImproperlyConfigured(
                'url_module should contain a list-typed urlpattern variable'
            )

    def detectURL(self, headURL = '', itertime=0):
        """
        get url
        :headURL :the former URL which need to be merged
        :return: (url,url_module)
        """
        from tornado.web import URLSpec
        urlList = []
        # print urlList
        for it in self.patterns:
            if isinstance(it,URLSpec):
                urlList.append(it)
                continue
            else:
                url,url_module = it

            # iterable get the URL
            if isinstance(url_module,urlPackage):
                # BFS get URL then extend it
                urlList.extend(url_module.detectURL(headURL='%s%s' %(headURL,url),itertime=itertime+1))
            elif isinstance(url_module,str):
                #print url_module
                # for individual one then add it to the list
                if headURL:
                    assemblyURL = '%s%s' %(headURL,url)
                else:
                    assemblyURL = '%s' %url
                    # convert it to URLSpec
                urlList.append(URLSpec(assemblyURL,url_module,name=url_module))
                # set up mapper for
                self.URLMapper[url_module] = assemblyURL
            else:
                raise ImproperlyConfigured('URL only accept string or URLpackage object(you can use include)')
        return urlList

    def getURLByHandler(self,name):
        return self.URLMapper.get(name)

    def get_url_by_handler(self,handler):
        import re
        for url,moduleStr in self.detectURL():
            if moduleStr == handler:
                purifyURL = re.match(r'\W+(/.+)$',url)
                return purifyURL.group(1)
        return None

def include(urlModules):
    """
    include modules then return all of their package
    :param arg:
    :param namespace:
    :param app_name:
    :return: urlPackage
    """
    '''
    if isinstance(urlModules,str):
        try :
            urlconf_module = import_module(urlModules)
        except:
            raise ImproperlyConfigured(
                'Cannot configure the url pattern successfully'
            )
    else:
        # try to get package
        urlconf_module = urlModules
    '''
    # get pattern from configured file


    # for configure
    return urlPackage(urlModules)


class templateModuleFinder:
    def __init__(self):
        '''
        init conf object and get searched path
        :return:
        '''
        # get conf object
        from conf import setting
        Setting = setting()
        Setting._setup()
        self.searchApp = getattr(Setting._wrapped,'INSTALLED_APPS')

    @property
    def uiDict(self):
        if not self.searchApp:
            # return a null dict
            return {}
        else :
            returnedDict = {}
            for app in self.searchApp:
                appUrlPath = '%s.urls' %(app)
                appUrlConf = import_module(appUrlPath)
                appUIDict = getattr(appUrlConf,'UImodule',{})
                # traverse dict and try to import it
                if isinstance(appUIDict,dict):
                    # merge dict
                    returnedDict.update(appUIDict)
                else:
                    raise ImproperlyConfigured('UImodule in %s should be configured in dict way' %(app) )
            return returnedDict


