#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.httpclient
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
import random

from tornado.options import define, options
from conf import conf
from picmd5 import filemd5
from thumbnail import thumb

define("port", default=conf.port, help="run on the given port", type=int)

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        ip = self.get_argument('ip', '255.255.255.255')
        t  = int(time.time())
        ip = str(ip)
        loc = 'pic_%s_%d'%(ip, t)
        if not os.path.exists(loc):
            os.makedirs(loc);
        file_metas  = self.request.files.get('file')
        filename = ''
        pic_loc  = ''
        if file_metas:
            meta = file_metas[0]
            filename = meta.get('filename', '')
        filepath = loc + '/' + filename
        if filename:
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            r = self.__handle(filepath)
            if not r:
                d = {'code':-1,'msg':'保存图片出错'}
                d = json.dumps(d)
                self.write(d)
            else:
                d = {'code':0, 'msg':'ok', 'data':r}
                d = json.dumps(d)
                self.write(d)
        else:
            d = {'code':-1,'msg':'没有图片名'}
            d = json.dumps(d)
            self.write(d)
        os.system('rm -rf ' + loc)

    def __handle(self, filepath):
        md5sum = filemd5(filepath)
        first  = md5sum[:10]
        second = md5sum[10:20]
        third  = md5sum[20:]
        name   = '%s/%s/%s/%s/' % (conf.picroot, first, second, third)
        if not os.path.exists(name):
            os.makedirs(name);
        r = thumb(filepath, name + '/%s'%conf.th_name , conf.th_y, conf.th_x)
        if not r:
            return []
        r = thumb(filepath, name + '/%s'%conf.name, conf.y, conf.x)
        if not r:
            return []
        return [first, second, third]

class WxUpHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        uid = self.get_argument('uid', None)
        src = self.get_argument('src', None)
        if not uid or not src:
            self.finish()
        else:
            http_client = tornado.httpclient.AsyncHTTPClient()
            resp = yield tornado.gen.Task(http_client.fetch, src)

            loc = 'uid_%s'%uid
            if not os.path.exists(loc):
                os.makedirs(loc);
            filepath = loc + '/2_600×800.jpg'
            with open(filepath, 'wb') as up:
                up.write(resp.body)
            r = self.__handle(filepath)
            print(r)
            os.system('rm -rf ' + loc)
    
            url='http://%s:%s/img' % (conf.dbserver_ip, conf.dbserver_port)
            headers = self.request.headers
            body = 'f=%s&s=%s&t=%s&k=1&uid=%s' % (r[0], r[1], r[2], uid)
            http_client = tornado.httpclient.AsyncHTTPClient()
            resp = tornado.gen.Task(
                http_client.fetch,
                url, 
                method='POST',
                headers=headers,
                body=body,
                validate_cert=False)
            self.finish()

    def __handle(self, filepath):
        md5sum = filemd5(filepath)
        first  = md5sum[:10]
        second = md5sum[10:20]
        third  = md5sum[20:]
        name   = '%s/%s/%s/%s/' % (conf.picroot, first, second, third)
        if not os.path.exists(name):
            os.makedirs(name);
        cmd = 'cp %s %s' % (filepath, name)
        os.system(cmd)
        return [first, second, third]

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
               (r'/wxup', WxUpHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
