#-*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
import json
import time
import datetime
import re
from tornado.options import define, options
from conf import conf
from picmd5 import filemd5
from thumbnail import thumb

define("port", default=conf.port, help="run on the given port", type=int)

def retcode(code, val):
    return {'code':code, 'md5':val}

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("mobile")
    def get_role(self):
        return int(self.get_secure_cookie("role"))

class AddHandler(BaseHandler):
    def get(self):
        self.render('up.html')
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        ip = self.request.remote_ip
        t  = str(time.time())
        ip = str(ip)
        loc = '%s_%s'%(ip, t)
        if not os.path.exists(loc):
            os.makedirs(loc);
        file_metas  = self.request.files.get('file')
        filename = ''
        pic_loc  = ''
        if file_metas:
            meta = file_metas[0]
            filename = meta.get('filename', '')
        print("filename=", filename)
        filepath = loc + '/' + filename
        if filename:
            yield tornado.gen.Task(self.__up_img, filepath, meta['body'])
            r = self.__handle(filepath)
            if not r:
                ret = retcode(-1, -1)
                self.write(ret)
            else:
                ret = retcode(0, r)
                self.write(ret)
        else:
            ret = retcode(-1, -1)
            self.write(ret)
        os.system('rm -rf ' + loc)
        self.finish()

    @tornado.gen.coroutine
    def __up_img(self, name, body):
        with open(name, 'wb') as up:
            up.write(body)
    def __handle(self, filepath):
        md5sum = filemd5(filepath)
        first  = md5sum[:10]
        second = md5sum[10:20]
        third  = md5sum[20:]
        name   = '%s/%s/%s/%s/' % (conf.picroot, first, second, third)
        if not os.path.exists(name):
            os.makedirs(name);
        r = thumb(filepath, name + '/1.jpg', 600, 800)
        if not r:
            return None
        r = thumb(filepath, name + '/2.jpg', 300, 400)
        if not r:
            return None
        return md5sum

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        "debug":True}
    handler = [
               (r'/up', AddHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
