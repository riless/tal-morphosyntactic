#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web

import handlers
import os


settings = dict({
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__),"templates"),
    "cookie_secret": os.urandom(12),
    "login_url": "/login",
    "xsrf_cookies": False,
    "debug":True
})

urls = [
    (r"/", handlers.MainHandler),
    (r"/analyzer/.*", handlers.Analyzer),
]

application = tornado.web.Application(urls, **settings)

if __name__ == "__main__":
    application.listen(8888, "0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()