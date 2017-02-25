# -*- coding: utf-8 -*-
# filename: main.py

import web
from handle import Handle
from basic import Basic
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urls = (
    '/wx', 'Handle',
)
     
if __name__ == '__main__':

#    Basic.__init__(Basic)
#    Basic.run(Basic);

    app = web.application(urls, globals())
    app.run()


