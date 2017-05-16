# -*- coding: UTF-8 -*-
# author = kidozh

from core.requestHandler import BaseHandler

class docRequestHandler(BaseHandler):
    def get(self,docname,*args,**kwargs):
        if docname not in ['deustch_score_transfer']:
            self.write_error(404)
            return
        try:
            self.render('usefulTools/%s.html' % (docname),*args)
        except Exception as e:
            raise e
            self._reason = '瞄~'
            self.write_error(404)