#coding=utf8

import json
import tornado.ioloop
import tornado.web
from .wsdl import Soap

class MainHandler(tornado.web.RequestHandler):
    config = {}

    @classmethod
    def setconfig(cls, config):
        cls.config = config

    def get(self):
        if 'wsdl' in self.request.arguments:
            self.set_header( 'Content-Type', 'text/xml' )
            with open('./wsdl.xml') as f:
                return self.write(f.read())
        self.write(json.dumps(MainHandler.config, indent=4))

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
            self.write(f.read())


def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])


def start_server(port, config):
    app = make_app()
    app.listen(int(port))
    MainHandler.setconfig(config)
    tornado.ioloop.IOLoop.current().start()
