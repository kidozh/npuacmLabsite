# -*- coding: UTF-8 -*-
# author = kidozh

urlpatterns = [
    ('/','notification.view.indexPageRequestHandler'),
    ('/post/(\d*?)','notification.view.postPageRequestHandler')

]