#coding=utf8

import json
import tornado.ioloop
import tornado.web
import tornado.escape
from .wsdl import Soap

class MainHandler(tornado.web.RequestHandler):
    config = {}

    @classmethod
    def setconfig(cls, config):
        cls.config = config

    def get(self):
        if 'wsdl' in self.request.arguments:
            with open('./wsdl.xml') as f:
                wsdl = f.read()
                self.set_header( 'Content-Type', 'application/xml charset=utf-8' )
                self.finish(wsdl)
        else:
            config = json.dumps(MainHandler.config, indent=4)
            self.set_header( 'Content-Type', 'application/json charset=utf-8' )
            self.finish(config)

    def post(self):
        url = self.request.path[1:]
        if url not in MainHandler.config:
            return self.write(f"url:{url} not match any service")
        soap = Soap(self.request.body)
        port = soap.port_name()
        ports = MainHandler.config[url]
        if port not in ports:
            return self.write(f"invalid method {port}")
        file_path = ports[port]
        with open(file_path, 'r') as f:
            self.set_header( 'Content-Type', 'application/xml charset=utf-8' )
            self.finish(f.read())


def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])


def start_server(port, config):
    app = make_app()
    app.listen(int(port))
    MainHandler.setconfig(config)
    tornado.ioloop.IOLoop.current().start()
