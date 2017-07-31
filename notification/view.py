# -*- coding: UTF-8 -*-
# author = kidozh

from core.requestHandler import BaseHandler
from .models import *
import datetime
import time
import tornado.escape
import markdown

class indexPageRequestHandler(BaseHandler):
    '''
    use get to render main page
    use javascript(Vue) to finish contents rendering
    '''
    def get(self):
        self.render('notification/index.html')

    def post(self):
        # use ajax to crawl
        ret_dict = {}
        query_page_length = self.get_argument('query_page_length',10)
        query_page_num = self.get_argument('query_page_num',1)
        try:
            query_page_length = int(query_page_length)
            query_page_num = int(query_page_num)
        except:
            raise self.write_error(403)
            return
        # do database
        # pinned message first
        pinned_query = markdownNotice.filter(markdownNotice.is_top==True,markdownNotice.publish_status!='draft')\
            .order_by('publish_time')
        ret_dict['top_notice'] = []
        for notice in pinned_query:
            notice_dict = {}
            # print('#',notice.retrive_all_info())
            for name,attr in notice.retrive_all_info().items():

                if name == 'password':
                    # filter password information
                    continue
                else:
                    if isinstance(attr,datetime.datetime):
                        # convert to timestamp
                        # datetime -> time_tuple
                        attr = attr.timetuple()
                        # time_tuple -> timestamp
                        attr = time.mktime(attr)

                    notice_dict[name] = attr

            notice_dict['markdown_html'] = markdown.markdown(notice.markdown_cotent)
            ret_dict['top_notice'].append(notice_dict)
        ret_dict['notice'] = []
        # normal notice
        query = markdownNotice.filter(markdownNotice.is_top==False,markdownNotice.publish_status!='draft')\
            .order_by(markdownNotice.publish_time.desc())\
            .paginate(query_page_num,query_page_length)
        for notice in query:

            notice_dict = {}
            for name,attr in notice.retrive_all_info().items():

                if name == 'password':
                    # filter password information
                    continue
                else:
                    if isinstance(attr,datetime.datetime):
                        # convert to timestamp
                        # datetime -> time_tuple
                        attr = attr.timetuple()
                        # time_tuple -> timestamp
                        attr = time.mktime(attr)

                    notice_dict[name] = attr


            notice_dict['markdown_html'] = markdown.markdown(notice.markdown_cotent)
            ret_dict['notice'].append(notice_dict)
        self.write(tornado.escape.json_encode(ret_dict))
        self.finish()

from contrib.admin.view import BaseHandler as adminBaseHandler

class postPageRequestHandler(adminBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        '''
        render post page
        :param args: 
        :param kwargs: 
        :return: 
        '''
        change = False
        if(len(args)>=1) and args[0]:
            # need to query first
            notice_id = args[0]
            change = True
            changed_notice = markdownNotice.select().where(markdownNotice.id==notice_id).get()

            pass
        else:
            # execute new one
            pass
        codemirror_version='5.27.4'
        if change:
            next_notice_id = notice_id
        else:
            next_notice_id = markdownNotice.select().count()

        # search for draft
        draft_notice = markdownNotice.select().where(markdownNotice.publish_status=='draft')

        args = locals()
        args.pop('self')
        self.render('notification/post.html',**args)

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        change = False
        if (len(args) >= 1):
            # need to query first
            notice_id = args[0]
            change = True
            pass
        else:
            # execute new one
            pass

        title = self.get_argument('title')
        isTop = self.get_argument('is_top',False)
        isTop = True if isTop == '1' else False

        content = self.get_argument('content')
        publish_status = self.get_argument('publish_status','draft')

        if change:
            saved_notice = markdownNotice.get(id=notice_id)
            saved_notice.title = title
            saved_notice.is_top = isTop
            saved_notice.markdown_cotent = content
            saved_notice.publish_status = publish_status
        else:
            saved_notice,insert = markdownNotice.get_or_create(title=title,
                                                    is_top=isTop,
                                                    markdown_cotent=content,
                                                    publish_status=publish_status)
        saved_notice.save()


        # construct query

        # print(title,isTop)
        self.redirect(self.reverse_url('notification.view.indexPageRequestHandler'))
        # self.write('Your article has been accepted.')
        # self.finish()


class apiQueryRequestHandler(adminBaseHandler):
    # need auth!!!
    def get(self,*args,**kwargs):
        query = self.get_argument('notice_type','draft')
        # use draft by default
        query = 'draft'